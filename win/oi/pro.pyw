import json, argparse

class Problem():
    
    def __init__(self):
        self.problemsFile = "C:/Users/me/desktop/pro.txt"
        self.list = []
    
    def getList(self):
        with open(self.problemsFile, 'r') as f:
            cc = json.loads(f.read())
        self.list = cc
    
    def updateList(self):
        with open(self.problemsFile, 'w') as f:
            f.write(json.dumps(self.list, indent=4))
 
    def add(self, p):
        self.list.append(p)
    
    def solve(self, p):
        self.list.remove(p)
    
    def cli(self): # Make an args parser
        my_parser = argparse.ArgumentParser(prog= "Problem")

        my_parser.add_argument('problem', action='store', type=str)
        my_parser.add_argument('-s', '--solve', action= 'store_true')
        my_parser.add_argument('-a','--add', action = 'store_true')
        my_parser.add_argument('-l', '--list', action= 'store_true')
        args = my_parser.parse_args()
            
        if(args.problem == "list"):
            self.getList()
            return ("\n").join(self.list)
        
        if(args.add or (args.add + args.solve + args.list) == 0):
            self.getList()
            if(args.problem in self.list):
                return "Problem already exists!"

            self.add(args.problem)
            self.updateList()
            return f"{args.problem} added!"
        
        if(args.solve):
            self.getList()
            if(args.problem not in self.list):
                return "Problem not found."

            self.solve(args.problem)
            self.updateList()
            return f"{args.problem} solved!"
        
        if(args.list and (args.add + args.solve) == 0):
            self.getList()
            return ('\n').join(self.list)

    def run_cli(self):
        return self.cli()

if __name__ == "__main__":
    rs = Problem().run_cli()
    print(rs)