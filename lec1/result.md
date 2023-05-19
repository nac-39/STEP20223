# 実行結果

## 1. score_checker ではなく max で比較していたバージョン

You answer is correct! Your score is 193.  
You answer is correct! Your score is 18643.  
You answer is correct! Your score is 221999.

## 2. score_checker を使うようになったバージョン

small:  
time: 5.045994250001968s  
You answer is correct! Your score is 193.  
medium:  
time: 323.4841967919929s  
You answer is correct! Your score is 18911.

large:  
time: 3721.087472542s  
You answer is correct! Your score is 244642.

## 3. dict を使うようにしたバージョン

(ここまで、アナグラムを調べるたびに辞書を並び替えていた…)

small:  
time: 2.695723374999943s  
You answer is correct! Your score is 193.

medium:  
You answer is correct! Your score is 18911.  
time: 287.2076153750095s

large:  
The number of words in large.txt and large_answer.txt doesn't match.  
time: 3146.746209332996s

## 4. 先に辞書を並べ替えるようにした

large が劇的に早くなった！  
small time: 0.014160958002321422s  
medium time: 2.130765624984633s  
large time: 2.771617791004246s

## small, medium に 16 字以下の辞書を使うようにしてもそこまで速度は変わらない

-- small,medium に normal_dictionary を適用  
small time: 0.014625042007537559s  
medium time: 2.1910829580156133s  
small time: 0.014717165991896763s  
medium time: 2.181812249997165s  
small time: 0.014902374998200685s  
medium time: 2.249973250000039s

-- small,medium に small_dictionary を適用  
small time: 0.040003208006964996s  
medium time: 2.660390125005506s  
small time: 0.01415712499874644s  
medium time: 2.095719749981072s  
small time: 0.014182249986333773s  
medium time: 2.184658499987563s
