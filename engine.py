from parser import MyParse
import os
schema = []
tables = []
operations = ["sum","average","max","min"]
def init_engine():
    ot = open("content/welcome.txt","r")
    print ot.read(),
    l = open("metadata.txt","r")
    l = l.read()
    l = l.split("<begin_table>")
    for i in l:
        if len(i):
            schema.append(i.split()[:-1])
            tables.append(i.split()[0])
    print tables
    print schema
    return

def find_table(table_name):
    global tables
    for x in tables:
        if x == table_name:
            return tables.index(x)
    return -1

def find_column(tno,column_name):
    global schema
    table = schema[tno][1:]
    for col in table:
        if col == column_name:
            return table.index(col)
    return -1


def kill_engine():
    ct = open("content/bye.txt","r")
    print ct.read(),
    return


def print_data(cols,tno):
    #print cols
    global tables
    global schema
    data = []
    temp= open(tables[tno] + '.csv','r')
    temp = temp.read()
    temp = temp.split('\n')
    table = []
    for x in temp:
        table.append(x.strip().split(','))
    for m in cols[:-1]:
        print tables[tno] + '.' + str(schema[tno][m+1])+',',
    print tables[tno] + '.' + str(schema[tno][cols[-1] + 1])

    for row in table:
        temp = []
        for l in  cols:
            temp.append(row[l])
        data.append(temp)
    for row in data:
        for col in row[:-1]:
            print col + ',',
        print row[-1]
    return

def process(a):
    global tables
    if 1:
        if len(a.tables) == 1:
            tno = find_table(a.tables[0])
            if not tno == -1:
                cols = []
                error_found = 0
                if len(a.columns) == 1 and a.columns[0] == "*":
                    cols = range(len(schema[tno])-1)
                else:
                    print "table no " + str(tno)
                    for col in a.columns:
                        print a.columnssq
                        if find_column(tno,col) == -1:
                            print "One or more columns cannot be found in the table"
                            error_found = 1
                            break
                        else:
                            cols.append(find_column(tno,col))
                if not error_found:
                    print_data(cols,tno)
                return
            else:
                print "The table " + a.tables[0] + "  is not found."
        else:
            print "Input a table name."
    else:
        print "where condition is not there"
    return 

def run_engine():
    prompt  = ">>>  "
    while 1:
        x = raw_input(prompt)
        if x.strip() in ["exit","quit"] and len(x):
            break
        if x.strip() in ["clear","cc"]:
            os.system("clear")
        elif len(x):
            a = MyParse(x)
            if not a == 0:
                print a
                process(a)

            
        else:
            pass

if __name__ == "__main__":
    init_engine()
    run_engine()
    kill_engine()
