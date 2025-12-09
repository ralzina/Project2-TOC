from src.helpers.turing_machine import TuringMachineSimulator


# ==========================================
# PROGRAM 1: Nondeterministic TM [cite: 137]
# ==========================================
class NTM_Tracer(TuringMachineSimulator):
    def run(self, input_string, max_depth):
        """
        Performs a Breadth-First Search (BFS) trace of the NTM.
        Ref: Section 4.1 "Trees as List of Lists" [cite: 146]
        """
        
        print("---------------------------------")
        print(f"Tracing NTM: {self.machine_name} on input '{input_string}'")
        print("---------------------------------")

        # Initial Configuration: ["", start_state, input_string]
        # Note: Represent configuration as quads (prev_state, left, curr_state, right) [cite: 156]
        initial_config = [None,"", self.start_state, "$" + input_string + "_"]

        # The tree is a list of lists of configurations
        tree = [[initial_config]]

        depth = 0
        accepted = False

        total_configs = 0
        considered_configs = 0

        while depth < max_depth and not accepted:
            current_level = tree[-1]
            next_level = []
            all_rejected = True

            # print("-----------")

            # TODO: STUDENT IMPLEMENTATION NEEDED
            # 1. Iterate through every config in current_level.
            # 2. Check if config is Accept (Stop and print success) [cite: 179]
            # 3. Check if config is Reject (Stop this branch only) [cite: 181]
            # 4. If not Accept/Reject, find valid transitions in self.transitions.
            # 5. If no explicit transition exists, treat as implicit Reject.
            # 6. Generate children configurations and append to next_level[cite: 148].

            for config in current_level:
                # Check accept, if accept stop and print success

                prev_state = config[2]

                if config[2] in self.accept_states:
                    print("ACCEPTED string: " + input_string + " after " + str(total_configs) + " transitions and depth " + str(depth) + ".")
                    print("Level of nondeterminisim: " + f"{total_configs/considered_configs:.2f}")
                    self.print_trace_path(tree,config[2])
                    return

                # Check reject, if reject continue and don't add to next level
                if config[2] == self.reject_state:
                    continue
                    
                # print(config)
                for transition in self.get_transitions(config[2],config[3][0]):
                    if transition['move'][0] == "L":
                        left = config[1][:-1]
                        right = config[1][-1] + transition['write'][0] + config[3][1:] if config[1] else transition['write'][0] + config[3][1:]
                    elif transition['move'][0] == "R":
                        left = config[1] + transition['write'][0]
                        right = config[3][1:]
                    elif transition['move'][0] == "S":
                        left = config[1]
                        right = transition['write'][0] + config[3][1:]
                    
                    next_state = transition['next']

                    next_level.append([prev_state,left,next_state,right])
                    total_configs += len(next_level)

            # Placeholder for logic:
            if not next_level and all_rejected:
                # TODO: Handle "String rejected" output [cite: 258]
                print("REJECTED string: " + input_string + " after " + str(total_configs) + " transitions and depth " + str(depth) + ".")
                if total_configs > 0 and considered_configs > 0:
                    print("Level of nondeterminisim: " + f"{total_configs/considered_configs:.2f}")
                self.print_trace_path(tree,current_level[0][2])
                return
            
            considered_configs += len(current_level) 
            

            tree.append(next_level)
            depth += 1

        if depth >= max_depth:
            print(f"Execution stopped after {max_depth} steps.")  # [cite: 259]

    def print_trace_path(self, tree, final_node):
        """
        Backtrack and print the path from root to the accepting node.
        Ref: Section 4.2 [cite: 165]
        """

        # Find correct path
        path = [node[0][0] for node in tree][2:]
        # print(path)

        # Reconstruct path in polynomial time as any DFA could

        config = tree[0][0][1:]

        i = 0

        print("---------------------------------")
        print("Traceback:")

        while i < len(path) + 1:
            print(config[0] + " " + config[1] + " " + config[2])

            for transition in self.get_transitions(config[1],config[2][0]):
                if (i < len(path) and transition["next"] == path[i]) or transition["next"] == final_node:
                    if transition['move'][0] == "L":
                        left = config[0][:-1]
                        right = config[0][-1] + transition['write'][0] + config[2][1:] if config[0] else transition['write'][0] + config[2][1:]

                    elif transition['move'][0] == "R":
                        left = config[0] + transition['write'][0]
                        right = config[2][1:]

                    elif transition['move'][0] == "S":
                        left = config[0]
                        right = transition['write'][0] + config[2][1:]
                    
                    next_state = transition['next']

                    config = [left,next_state,right]

                    # stop loop if reached final state
                    if transition['next'] == final_node:
                        i = len(path) + 1

            i+=1
                    
        print(config[0] + " " + config[1] + " " + config[2])

        print("---------------------------------")
        
