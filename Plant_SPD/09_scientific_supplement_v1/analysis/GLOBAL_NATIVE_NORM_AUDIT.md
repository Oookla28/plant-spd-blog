# E08全局范数口径核查

**结论：没有把69个类别行的最大范数误当成完整分类头范数。**

源码先将两个视图、全部69类的W与b拼成73002维theta，再计算theta@theta。M的max跨四个完整native分类器，而不是跨类别行。正则项也对同一完整theta计算lambda/2*theta@theta；W和b的梯度均包含lambda乘参数。

M=1598050.0561，lambda=1.251525252518626e-08。四个native罚项都不超过0.01，故不需要额外乘69；不能据此声称HELD或100%训练准确率得到保证。

数值与源码SHA见GLOBAL_NATIVE_NORM_AUDIT.json。原数据、权重、预测、协议均未修改。
