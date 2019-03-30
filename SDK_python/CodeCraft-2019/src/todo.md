1. python3.7(3.6)在新算法的answer输出与之前一样，所以调度的结果是1100。
2. python3.5在新算法的answer输出与之前不一样，所以调度结果为1102，官方结果也是1102。
    所以唯一的问题，就是python3.7(3.6)的dict顺序与用户填入时不一致，导致输出的answer不一致。
    
    
1. t:394  max_car_num:80  fill_rate:0.26 deadlock
2. t:488  max_car_num:25  fill_rate:0.26