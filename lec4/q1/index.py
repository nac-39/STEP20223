import sys
import collections


class Wikipedia:
    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):
        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()

    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()

    # Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()

    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    def find_shortest_path(self, start, goal, print_path=True):
        for k, v in self.titles.items():
            if v == start:
                start = k
            if v == goal:
                goal = k
        if type(start) == str or type(goal) == str:
            print("The title is not found.")
            return "Not found"
        queue = collections.deque()
        visited = {}
        visited[start] = True
        queue.append([start])
        while not len(queue) == 0:
            node = queue.popleft()
            if node[-1] == goal:
                shortest_path = [self.titles[i] for i in node]
                if print_path:
                    print("The shortest path is:")
                    print(" -> ".join(shortest_path))
                return shortest_path
            for child in self.links[node[-1]]:
                if not child in visited:
                    visited[child] = True
                    queue.append(node + [child])
        print(f"The path {self.titles[start]} -> {self.titles[goal]} is not found.")
        return "Not found"

    # Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        # ------------------------#
        # Write your code here!  #
        # ------------------------#
        pass

    # Do something more interesting!!
    def find_something_more_interesting(self):
        # ------------------------#
        # Write your code here!  #
        # ------------------------#
        pass


def test_small():
    wikipedia = Wikipedia(
        "./lec4/wikipedia_dataset/pages_small.txt",
        "./lec4/wikipedia_dataset/links_small.txt",
    )
    assert wikipedia.find_shortest_path("A", "B", print_path=False) == ["A", "B"]
    assert wikipedia.find_shortest_path("A", "C", print_path=False) == ["A", "B", "C"]
    assert wikipedia.find_shortest_path("C", "A", print_path=False) == ["C", "A"]
    assert wikipedia.find_shortest_path("A", "E", print_path=False) == ["A", "B", "C", "E"]
    assert wikipedia.find_shortest_path("A", "F", print_path=False) == ["A", "B", "C", "F"]
    print("test_small() passed!")


if __name__ == "__main__":
    test_small()
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # wikipedia.find_longest_titles()
    # wikipedia.find_most_linked_pages()
    
    wikipedia.find_shortest_path("言語学", "イラク")
    wikipedia.find_shortest_path("渋谷", "パレートの法則")
    wikipedia.find_shortest_path("渋谷", "アース・ウィンド・アンド・ファイアー")
    wikipedia.find_shortest_path("ノーム・チョムスキー", "コンパイラ")
    wikipedia.find_shortest_path("統計力学", "奈良線")
    wikipedia.find_shortest_path("コンピュータ・アーキテクチャ", "ワンダフルライフ_(映画)")
    wikipedia.find_shortest_path("コンピュータ・アーキテクチャ", "小林賢太郎")
    wikipedia.find_shortest_path("コンピュータ・アーキテクチャ", "ユーゴスラビア改名")
    # wikipedia.find_most_popular_pages()
