# Retrieval Benchmark Results

## Summary

| collection | total_chunks_db | top_k | queries | hit_rate | mrr | avg_latency_ms |
| --- | --- | --- | --- | --- | --- | --- |
| scientific_articles | 109 | 1 | 3 | 0.0% | 0.000 | 91.5 |
| scientific_articles | 109 | 3 | 3 | 0.0% | 0.000 | 133.1 |
| scientific_articles | 109 | 5 | 3 | 33.3% | 0.083 | 47.7 |

## Detail

| collection | total_chunks_db | top_k | query_id | query_type | doi | hit | first_hit_rank | avg_score | latency_ms | context_chars | top_sections | query |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| scientific_articles | 109 | 1 | q1 | factoid | 10.1016/j.undsp.2024.04.008 | no |  | 0.4138 | 126.6 | 209 | Junfeng Sun[a] , Yong Fang[a][,][⇑] , Hu Luo[a] , Zhigang Yao[a] , Long Xiang[b] , Jianfeng Wang[a] , Yubo Wang[a] , Yifan Jiang[a] | What is the main contribution of this paper? |
| scientific_articles | 109 | 1 | q2 | method | 10.1016/j.undsp.2024.04.008 | no |  | 0.2887 | 42.8 | 437 | Junfeng Sun[a] , Yong Fang[a][,][⇑] , Hu Luo[a] , Zhigang Yao[a] , Long Xiang[b] , Jianfeng Wang[a] , Yubo Wang[a] , Yifan Jiang[a] | What method is proposed in this paper? |
| scientific_articles | 109 | 1 | q3 | result | 10.1016/j.undsp.2024.04.008 | no |  | 0.3577 | 105.0 | 140 | Junfeng Sun[a] , Yong Fang[a][,][⇑] , Hu Luo[a] , Zhigang Yao[a] , Long Xiang[b] , Jianfeng Wang[a] , Yubo Wang[a] , Yifan Jiang[a] | What are the main experimental results? |
| scientific_articles | 109 | 3 | q1 | factoid | 10.1016/j.undsp.2024.04.008 | no |  | 0.3144 | 37.0 | 1722 | Junfeng Sun[a] , Yong Fang[a][,][⇑] , Hu Luo[a] , Zhigang Yao[a] , Long Xiang[b] , Jianfeng Wang[a] , Yubo Wang[a] , Yifan Jiang[a] | What is the main contribution of this paper? |
| scientific_articles | 109 | 3 | q2 | method | 10.1016/j.undsp.2024.04.008 | no |  | 0.2806 | 296.8 | 1126 | Junfeng Sun[a] , Yong Fang[a][,][⇑] , Hu Luo[a] , Zhigang Yao[a] , Long Xiang[b] , Jianfeng Wang[a] , Yubo Wang[a] , Yifan Jiang[a] | What method is proposed in this paper? |
| scientific_articles | 109 | 3 | q3 | result | 10.1016/j.undsp.2024.04.008 | no |  | 0.3444 | 65.5 | 414 | Junfeng Sun[a] , Yong Fang[a][,][⇑] , Hu Luo[a] , Zhigang Yao[a] , Long Xiang[b] , Jianfeng Wang[a] , Yubo Wang[a] , Yifan Jiang[a]; Unknown; ScienceDirect | What are the main experimental results? |
| scientific_articles | 109 | 5 | q1 | factoid | 10.1016/j.undsp.2024.04.008 | no |  | 0.2864 | 51.5 | 2674 | Junfeng Sun[a] , Yong Fang[a][,][⇑] , Hu Luo[a] , Zhigang Yao[a] , Long Xiang[b] , Jianfeng Wang[a] , Yubo Wang[a] , Yifan Jiang[a]; ScienceDirect | What is the main contribution of this paper? |
| scientific_articles | 109 | 5 | q2 | method | 10.1016/j.undsp.2024.04.008 | no |  | 0.2694 | 50.9 | 2504 | Junfeng Sun[a] , Yong Fang[a][,][⇑] , Hu Luo[a] , Zhigang Yao[a] , Long Xiang[b] , Jianfeng Wang[a] , Yubo Wang[a] , Yifan Jiang[a] | What method is proposed in this paper? |
| scientific_articles | 109 | 5 | q3 | result | 10.1016/j.undsp.2024.04.008 | yes | 4 | 0.3131 | 40.6 | 1343 | Junfeng Sun[a] , Yong Fang[a][,][⇑] , Hu Luo[a] , Zhigang Yao[a] , Long Xiang[b] , Jianfeng Wang[a] , Yubo Wang[a] , Yifan Jiang[a]; Unknown; ScienceDirect | What are the main experimental results? |

