import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class OptimalBST:
    def __init__(self, keys, freq):
        """
        Initialize OBST with keys and their frequencies
        
        Args:
            keys: List of keys in sorted order
            freq: List of frequencies corresponding to each key
        """
        self.keys = keys
        self.freq = freq
        self.n = len(keys)
        
        # DP tables
        self.cost = [[0 for _ in range(self.n)] for _ in range(self.n)]
        self.root = [[0 for _ in range(self.n)] for _ in range(self.n)]
        
    def construct_obst(self):
        """
        Construct Optimal BST using Dynamic Programming
        Returns the minimum cost
        """
        # Initialize cost for single keys
        for i in range(self.n):
            self.cost[i][i] = self.freq[i]
            self.root[i][i] = i
        
        # Build cost table for chains of increasing length
        for length in range(2, self.n + 1):
            for i in range(self.n - length + 1):
                j = i + length - 1
                self.cost[i][j] = float('inf')
                
                # Calculate sum of frequencies from i to j
                freq_sum = sum(self.freq[i:j+1])
                
                # Try all possible roots and find minimum cost
                for r in range(i, j + 1):
                    # Cost of left subtree
                    left_cost = self.cost[i][r-1] if r > i else 0
                    # Cost of right subtree
                    right_cost = self.cost[r+1][j] if r < j else 0
                    
                    # Total cost with r as root
                    total_cost = left_cost + right_cost + freq_sum
                    
                    if total_cost < self.cost[i][j]:
                        self.cost[i][j] = total_cost
                        self.root[i][j] = r
        
        return self.cost[0][self.n-1]
    
    def print_cost_matrix(self):
        """Print the cost matrix in a formatted way"""
        print("\n" + "="*60)
        print("COST MATRIX")
        print("="*60)
        print(f"{'':>8}", end='')
        for j in range(self.n):
            print(f"{self.keys[j]:>8}", end='')
        print()
        print("-" * 60)
        
        for i in range(self.n):
            print(f"{self.keys[i]:>8}", end='')
            for j in range(self.n):
                if j >= i:
                    print(f"{self.cost[i][j]:>8.1f}", end='')
                else:
                    print(f"{'':>8}", end='')
            print()
        print("="*60)
    
    def print_root_matrix(self):
        """Print the root matrix showing optimal root for each subproblem"""
        print("\n" + "="*60)
        print("ROOT MATRIX (Shows optimal root index for each range)")
        print("="*60)
        print(f"{'':>8}", end='')
        for j in range(self.n):
            print(f"{self.keys[j]:>8}", end='')
        print()
        print("-" * 60)
        
        for i in range(self.n):
            print(f"{self.keys[i]:>8}", end='')
            for j in range(self.n):
                if j >= i:
                    print(f"{self.keys[self.root[i][j]]:>8}", end='')
                else:
                    print(f"{'':>8}", end='')
            print()
        print("="*60)
    
    def get_tree_structure(self, i, j, parent=None, is_left=None):
        """
        Recursively build tree structure
        Returns list of (node, parent, is_left) tuples
        """
        if i > j:
            return []
        
        root_idx = self.root[i][j]
        root_key = self.keys[root_idx]
        
        result = [(root_key, parent, is_left)]
        
        # Left subtree
        result.extend(self.get_tree_structure(i, root_idx - 1, root_key, True))
        
        # Right subtree
        result.extend(self.get_tree_structure(root_idx + 1, j, root_key, False))
        
        return result
    
    def print_tree_structure(self):
        """Print tree structure in a readable format"""
        print("\n" + "="*60)
        print("OPTIMAL BINARY SEARCH TREE STRUCTURE")
        print("="*60)
        
        tree_nodes = self.get_tree_structure(0, self.n - 1)
        
        # Get root
        root = tree_nodes[0][0]
        print(f"\nRoot: {root}")
        
        # Print other nodes
        for node, parent, is_left in tree_nodes[1:]:
            direction = "left" if is_left else "right"
            print(f"  {node} is {direction} child of {parent}")
        
        print("="*60)
    
    def visualize_tree(self):
        """Create a visual representation of the OBST"""
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        def draw_node(ax, key, x, y, level, x_offset):
            """Draw a node and its connections"""
            # Draw circle
            circle = patches.Circle((x, y), 0.3, facecolor='lightblue', 
                                   edgecolor='black', linewidth=2)
            ax.add_patch(circle)
            
            # Draw text
            ax.text(x, y, str(key), ha='center', va='center', 
                   fontsize=12, fontweight='bold')
            
            return x, y
        
        def draw_tree(i, j, x, y, level, x_offset):
            """Recursively draw the tree"""
            if i > j:
                return
            
            root_idx = self.root[i][j]
            root_key = self.keys[root_idx]
            
            # Draw current node
            node_x, node_y = draw_node(ax, root_key, x, y, level, x_offset)
            
            # Calculate positions for children
            new_x_offset = x_offset / 2
            
            # Draw left subtree
            if root_idx > i:
                left_x = x - x_offset
                left_y = y - 1.5
                ax.plot([node_x, left_x], [node_y - 0.3, left_y + 0.3], 
                       'k-', linewidth=1.5)
                draw_tree(i, root_idx - 1, left_x, left_y, level + 1, new_x_offset)
            
            # Draw right subtree
            if root_idx < j:
                right_x = x + x_offset
                right_y = y - 1.5
                ax.plot([node_x, right_x], [node_y - 0.3, right_y + 0.3], 
                       'k-', linewidth=1.5)
                draw_tree(root_idx + 1, j, right_x, right_y, level + 1, new_x_offset)
        
        # Start drawing from root
        draw_tree(0, self.n - 1, 5, 9, 0, 2)
        
        plt.title("Optimal Binary Search Tree Visualization", 
                 fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig('obst_tree.png', dpi=300, bbox_inches='tight')
        print("\n✓ Tree visualization saved as 'obst_tree.png'")
        plt.show()


def run_demo():
    """Run a demonstration with sample data"""
    print("\n" + "="*60)
    print("OPTIMAL BINARY SEARCH TREE (OBST) - DEMO")
    print("="*60)
    
    # Sample data
    keys = [10, 20, 30, 40]
    freq = [4, 2, 6, 3]
    
    print(f"\nKeys:        {keys}")
    print(f"Frequencies: {freq}")
    
    # Create OBST instance
    obst = OptimalBST(keys, freq)
    
    # Construct OBST
    print("\n🔄 Constructing Optimal Binary Search Tree...")
    min_cost = obst.construct_obst()
    
    print(f"\n✓ Construction Complete!")
    print(f"\n🎯 MINIMUM SEARCH COST: {min_cost}")
    
    # Display matrices
    obst.print_cost_matrix()
    obst.print_root_matrix()
    
    # Display tree structure
    obst.print_tree_structure()
    
    # Visualize tree
    print("\n📊 Generating tree visualization...")
    obst.visualize_tree()


def run_custom():
    """Run with custom user input"""
    print("\n" + "="*60)
    print("OPTIMAL BINARY SEARCH TREE - CUSTOM INPUT")
    print("="*60)
    
    # Get input
    n = int(input("\nEnter number of keys: "))
    
    keys = []
    print(f"\nEnter {n} keys in sorted order:")
    for i in range(n):
        key = int(input(f"  Key {i+1}: "))
        keys.append(key)
    
    freq = []
    print(f"\nEnter frequencies for each key:")
    for i in range(n):
        f = int(input(f"  Frequency for key {keys[i]}: "))
        freq.append(f)
    
    # Create and solve OBST
    obst = OptimalBST(keys, freq)
    
    print("\n🔄 Constructing Optimal Binary Search Tree...")
    min_cost = obst.construct_obst()
    
    print(f"\n✓ Construction Complete!")
    print(f"\n🎯 MINIMUM SEARCH COST: {min_cost}")
    
    # Display results
    obst.print_cost_matrix()
    obst.print_root_matrix()
    obst.print_tree_structure()
    
    # Ask if user wants visualization
    vis = input("\nDo you want to visualize the tree? (y/n): ").lower()
    if vis == 'y':
        print("\n📊 Generating tree visualization...")
        obst.visualize_tree()


def main():
    """Main function to run the program"""
    print("\n" + "="*60)
    print("   OPTIMAL BINARY SEARCH TREE (OBST) IMPLEMENTATION")
    print("   Design and Analysis of Algorithms - Mini Project")
    print("="*60)
    
    while True:
        print("\n\nMENU:")
        print("1. Run Demo with Sample Data")
        print("2. Enter Custom Data")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            run_demo()
        elif choice == '2':
            run_custom()
        elif choice == '3':
            print("\n👋 Thank you for using OBST Implementation!")
            break
        else:
            print("\n❌ Invalid choice! Please try again.")


if __name__ == "__main__":
    main()