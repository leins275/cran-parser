import argparse
import logging

from src.dependency_tree import DependencyTree
     
def parse_depts_in_source_file(fname: str):
    dt = DependencyTree(fname)
    dt.parse_dependencies()        
    dt.save_results("./pkg_out.scv")


def main():
    logging.getLogger().setLevel(logging.INFO)
    parser = argparse.ArgumentParser(description="Parse R dependencies")
    parser.add_argument("-f", "--fname", 
                        help="Path to source file",
                        default="./pkg_in.csv")
    args = parser.parse_args()
    parse_depts_in_source_file(args.fname)

if __name__ == "__main__":
    main()