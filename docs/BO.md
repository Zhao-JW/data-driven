
**code: BOexample.py**

The below section gives some simple demonstration of the Bayesian optimization process. The algorithm explores the given noisy function according to its acquisition fucntion (Expected improvement in this case) repeadly to find the global minimum. As shown in subplot 1, at first the algorithm explores around. Then as shown in subplot 2 at iteration 20the algorithm converge to keep evaluating points around the minimum. The exploration-exploitation varible xi balances the efficiency and accuracy (to escape local minimum) of the algorithm, as shown in subplot 2 vs 3. The noisier the data the less certain the fitted gaussian process is, as shown in subplot 2 vs 4.

![alt text](BOexample.png)
