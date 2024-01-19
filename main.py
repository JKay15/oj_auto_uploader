from oj_auto_uploader.oj_prob_inserter import problem_inserter
books=['/Users/xiongjiangkai/Desktop/高等代数 蓝以中/',
       ]

for book in books:
    bookname=book.split('/')[-2]
    inserter=problem_inserter(book,bookname)
    inserter.run()
    print(bookname+"Done!")
