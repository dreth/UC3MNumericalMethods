\ Model CurveFitting
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  e_plus[1] + e_plus[2] + e_plus[3] + e_plus[4] + e_plus[5] + e_neg[1]
   + e_neg[2] + e_neg[3] + e_neg[4] + e_neg[5] + 0 z
Subject To
 deviations[1]: a + 29.7 b + e_plus[1] - e_neg[1] = 175.3
 deviations[2]: a + 29.5 b + e_plus[2] - e_neg[2] = 177.8
 deviations[3]: a + 31.4 b + e_plus[3] - e_neg[3] = 185.4
 deviations[4]: a + 31.8 b + e_plus[4] - e_neg[4] = 175.3
 deviations[5]: a + 27.6 b + e_plus[5] - e_neg[5] = 172.7
Bounds
 a free
 b free
End
