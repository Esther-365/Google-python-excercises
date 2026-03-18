import re
import sys
import glob

def extract_name(filename):
    name_dict ={}
    names = []
    try:
        with open(filename,"r") as word:
            text = word.read()

        regex = r"Popularity in \b((19|20)\d{2})\b" #This restricts the years to 1900-2099.
        result = re.search(regex,text)
        if result :
            year = result.group(1)
            #print(year)

        pattern = r"<td>(\d+)</td><td>(\w+)</td><td>(\w+)</td>"#This gets the rank, male name and female name all together in a tuple and returns a list of tuples.
        match = re.findall(pattern,text)
        #print(match)

        for n in match:
            rank,male,female = n #unpacks the content of the tuple
            if male not in name_dict or int(rank) < int(name_dict[male]): #check if the value exist of if it's less than what already exists
                name_dict[male] = rank
                
            if female not in name_dict or int(rank) < int(name_dict[female]):           
                name_dict[female] = rank
        #print(name_dict)

        names.append(str(year))
        for k in sorted(name_dict):
            #sorts the dictionary while looping
            names.append(f"{k} {name_dict[k]}")
        return names    
        
    except FileNotFoundError:
        raise Exception(f"Missing File: The path {filename} was not found")

#f = r"C:\Projects\google-python-exercises\babynames\baby1990.html"
#extract_name(f)

def main():
    argv = sys.argv[1:]
    if argv[0] == "--summaryfile":
        for n in argv[1:]:
            if '*' in n:
                glob_list = glob.glob(n)
                for i in glob_list:
                    my_lis = extract_name(i)
                    summary = "\n".join(my_lis) + "\n"
                    sum_path = i + ".summary"
                    with open(sum_path,"w",encoding = "utf-8") as file:
                        file.write(summary)         
            else:
                my_lis = extract_name(n)
                summary = "\n".join(my_lis) + "\n"
                sum_path = n + ".summary"
                with open(sum_path,"w",encoding = "utf-8") as file:
                    file.write(summary)           
            #print(summary)
    else:
        for n in argv:
            if '*' in n:
                glob.glob(n)
            my_list = extract_name(n)
            summary = "\n".join(my_list) + "\n"
            print(summary)

if __name__ == '__main__':
    #This means "only run `main()` if this file is being run directly, not imported by another file.
    main()
