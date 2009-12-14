# Copyright (C) 2009, Brad Beattie
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from plurality import Plurality
from pluralityAtLarge import PluralityAtLarge
from instantRunoffVote import InstantRunoffVote
from singleTransferableVote import SingleTransferableVote 
from rankedPairs import RankedPairs
from schulzeMethod import SchulzeMethod
import json, types, StringIO, traceback


class ElectionRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        try:
            # Parse the incoming data
            jsonData = json.loads(self.rfile.read(int(self.headers["content-length"])))
            
            # Assume we're looking for a single winner
            if "winners" not in jsonData:
                jsonData["winners"] = 1
                
            # Assume each ballot represents a single voter's preference
            newInput = []
            for ballot in jsonData["ballots"]:
                if type(ballot) is not types.DictType:
                    ballot = {"ballot":ballot}
                if "count" not in ballot:
                    ballot["count"] = 1
                newInput.append(ballot)
            jsonData["ballots"] = newInput           

            # Send the data to the requested voting system
            if jsonData["votingSystem"] in ["plurality", "fptp"]:
                response = Plurality.calculateWinner(jsonData["ballots"])
            if jsonData["votingSystem"] in ["pluralityAtLarge", "blockVoting"]:
                response = PluralityAtLarge.calculateWinner(jsonData["ballots"], jsonData["winners"])
            elif jsonData["votingSystem"] in ["irv", "instantRunoff"]:
                response = InstantRunoffVote.calculateWinner(jsonData["ballots"], jsonData["winners"])
            elif jsonData["votingSystem"] in ["stv", "singleTransferableVote"]:
                response = SingleTransferableVote.calculateWinner(jsonData["ballots"], jsonData["winners"])
            elif jsonData["votingSystem"] in ["rankedPairs", "tideman"]:
                response = RankedPairs.calculateWinner(jsonData["ballots"])
            elif jsonData["votingSystem"] in ["schulzeMethod"]:
                response = SchulzeMethod.calculateWinner(jsonData["ballots"])
            elif jsonData["votingSystem"] in ["schulzeSTV"]:
                raise Exception("Not yet implemented")
            else:
                raise
            
            # Ensure a response came back from the voting system
            if response == None:
                raise Exception("No voting system specified")
        except:
            fp = StringIO.StringIO()
            traceback.print_exc(1,fp)
            response = fp.getvalue()
            self.send_response(500)

        else:
            self.send_response(200)
            
        finally:
            response = json.dumps(self.__simplifyObject__(response))
            self.send_header("Content-type", "application/json")
            self.send_header("Content-length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)


    # json.dump() has a difficult time with certain object types
    def __simplifyObject__(self, object):
        if type(object) == types.DictType:
            newDict = {}
            for key in object.keys():
                value = self.__simplifyObject__(object[key])
                key = self.__simplifyObject__(key)
                newDict[key] = value
            return newDict
        elif type(object) == types.TupleType:
            return "|".join(object)
        elif type(object) == type(set()) or type(object) == types.ListType:
            newList = []
            for element in object:
                newList.append(self.__simplifyObject__(element))
            return newList
        else:
            return object

def main():
    try:
        server = HTTPServer(('', 8044), ElectionRequestHandler)
        print('Webservice running...')
        server.serve_forever()
    except KeyboardInterrupt:
        print('Webservice stopping...')
        server.socket.close()

if __name__ == '__main__':
    main()
