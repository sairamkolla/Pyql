from pyparsing import CaselessKeyword, delimitedList, Each, Forward, Group, \
        Optional, Word, alphas,alphanums, nums, oneOf, ZeroOrMore, quotedString

def MyParse(s):
    keywords = ["select", "from", "where", "group by", "order by", "and", "or"]
    [select, _from, where, groupby, orderby, _and, _or] = [ CaselessKeyword(word)
            for word in keywords ]
 
    table = column = Word(alphas)
    columns = Group(delimitedList(column))
    columnVal = (nums | quotedString)
 
    whereCond = (column + oneOf("= != < > >= <=") + columnVal)
    whereExpr = whereCond + ZeroOrMore((_and | _or) + whereCond)
 
    selectStmt = Forward().setName("select statement")
    selectStmt << (select +
            ('*' | columns).setResultsName("columns") +
            _from +
            table.setResultsName("table") +
            Optional(where + Group(whereExpr), '').setResultsName("where").setDebug(False) +
            Each([Optional(groupby + columns("groupby"),'').setDebug(False),
                Optional(orderby + columns("orderby"),'').setDebug(False)
                ])
            )
    return selectStmt.parseString(s)
 
#def log(sql, parsed):
#    print "##################################################"
#    print sql
#    print parsed.table
#    print parsed.columns
#    print parsed.where
#    print parsed.groupby
#    print parsed.orderby
 
#sqls = [
#        """select * from users where username='johnabc'""",
#        """SELECT * FROM users WHERE username='johnabc'""",
#        """SELECT * FRom users""",
#        """SELECT * FRom USERS""",
#        """SELECT * FROM users WHERE username='johnabc' or email='johnabc@gmail.com'""",
#        """SELECT id, username, email FROM users WHERE username='johnabc' order by email, id""",
#       """SELECT id, username, email FROM users WHERE username='johnabc' group by school""",
#        """SELECT id, username, email FROM users WHERE username='johnabc' group by city, school order by firstname, lastname"""
#        ]
 
#for sql in sqls:
#    log(sql, selectStmt.parseString(sql))
