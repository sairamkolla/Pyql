from parser import MyParse
import os
schema = []
tables = []
operations = ["sum","average","min","max"]
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

def sum_col(colno,tno):
    global tables
    sum = 0
    x = open(tables[tno] + '.csv','r')
    x = x.read()
    x = x.split('\n')
    for i in x:
        sum += int(i.strip().split(',')[colno])
    return sum

def average_col(colno,tno):
    global tables
    sum = 0
    x = open(tables[tno] + '.csv', 'r')
    x = x.read()
    x = x.split('\n')
    for i in x:
        sum += int(i.strip().split(',')[colno])
    return sum/len(x)

def min_col(colno,tno):
    global tables
    min_value = 10000000000
    x = open(tables[tno] + '.csv', 'r')
    x = x.read()
    x = x.split('\n')
    for i in x:
        num = int(i.strip().split(',')[colno])
        if num < min_value:
            min_value = num
    return min_value

def max_col(colno,tno):
    global tables
    max_value = -10000000000
    x = open(tables[tno] + '.csv', 'r')
    x = x.read()
    x = x.split('\n')
    for i in x:
        num = int(i.strip().split(',')[colno])
        if num > max_value:
            max_value = num
    return max_value


def col_single_op(cno,tno,op):
    global operations
    global schema
    options = {0:sum_col,
               1:average_col,
               2:min_col,
               3:max_col}
    value = options[op](cno,tno)
    print operations[op] + '(' + schema[tno][cno+1] + ')'
    print value
    return

def kill_engine():
    ct = open("content/bye.txt","r")
    print ct.read(),
    return


def print_data(cols,ops,tno):
    print cols
    print ops
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
                ops = []
                col_op_query = 0
                col_not_found = 0
                error_found = 0
                if len(a.columns) == 1 and a.columns[0] == "*":
                    cols = range(len(schema[tno])-1)
                    ops = [-1]*len(cols)
                elif len(a.columns[0].split('(')) == 2:
                    col_name = a.columns[0].split('(')[1][:-1]
                    if find_column(tno,col_name) == -1:
                        print "One or more columns cannot be found in the table"
                        col_not_found = 1
                        error_found = 1
                    else:
                        col_op_query = 1
                        col_single_op(find_column(tno,col_name),tno,operations.index(a.columns[0].split('(')[0]))


                else:
                    print "table no " + str(tno)
                    for col in a.columns:
                        op = 0
                        col_name = col
                        print a.columns
                        print col_name
                        if len(col.split('(')) == 2:
                            print "There is an error in the query.Please recheck"
                            error_found = 1
                        if find_column(tno,col_name) == -1:
                            print "One or more columns cannot be found in the table"
                            col_not_found = 1
                            break
                        else:
                            cols.append(find_column(tno,col_name))

                            if not op:
                                ops.append(-1)

                if not col_not_found and not error_found and not col_op_query:
                    print_data(cols,ops,tno)
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
