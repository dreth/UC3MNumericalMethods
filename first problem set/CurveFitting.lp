\ Model CurveFitting
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  e_plus[1] + e_plus[2] + e_plus[3] + e_plus[4] + e_plus[5] + e_plus[6]
   + e_plus[7] + e_neg[1] + e_neg[2] + e_neg[3] + e_neg[4] + e_neg[5]
   + e_neg[6] + e_neg[7] + 0 z
Subject To
 deviations[1]: a + 30.1 b + e_plus[1] - e_neg[1] = 176.2
 deviations[2]: a + 29.5 b + e_plus[2] - e_neg[2] = 176.8
 deviations[3]: a + 30.4 b + e_plus[3] - e_neg[3] = 184.2
 deviations[4]: a + 31.6 b + e_plus[4] - e_neg[4] = 173.2
 deviations[5]: a + 27.4 b + e_plus[5] - e_neg[5] = 172.8
 deviations[6]: a + 28.3 b + e_plus[6] - e_neg[6] = 174.1
 deviations[7]: a + 33.4 b + e_plus[7] - e_neg[7] = 180.5
Bounds
 a free
 b free
End
