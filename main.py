from oj_auto_uploader.oj_prob_inserter import problem_inserter
books=['/Users/xiongjiangkai/Desktop/随机过程初级教程 Karlin/',
       ]

# 别忘了需要一个a.zip
for book in books:
    bookname=book.split('/')[-2]
    inserter=problem_inserter(book,bookname)
    inserter.run()
    print(bookname+"Done!")
