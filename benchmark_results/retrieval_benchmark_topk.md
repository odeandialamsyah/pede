# Retrieval Benchmark Results

## Summary

| collection | total_chunks_db | top_k | queries | hit_rate | mrr | avg_latency_ms |
| --- | --- | --- | --- | --- | --- | --- |
| scientific_articles | 109 | 1 | 3 | 0.0% | 0.000 | 66.5 |
| scientific_articles | 109 | 3 | 3 | 0.0% | 0.000 | 23.1 |
| scientific_articles | 109 | 5 | 3 | 33.3% | 0.083 | 21.2 |
| scientific_articles | 109 | 10 | 3 | 33.3% | 0.083 | 20.3 |
| scientific_articles | 109 | 15 | 3 | 66.7% | 0.107 | 21.1 |
| scientific_articles | 109 | 20 | 3 | 66.7% | 0.107 | 21.5 |

## Detail

| collection | total_chunks_db | top_k | query_id | query_type | doi | hit | first_hit_rank | avg_score | latency_ms | context_chars | top_sections | query |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| scientific_articles | 109 | 1 | q1 | factoid | 10.1016/j.undsp.2024.04.008 | no |  | 0.4138 | 149.4 | 209 | Junfeng Sun[a] , Yong Fang[a][,][⇑] , Hu Luo[a] , Zhigang Yao[a] , Long Xiang[b] , Jianfeng Wang[a] , Yubo Wang[a] , Yifan Jiang[a] | What is the main contribution of this paper? |
| scientific_articles | 109 | 1 | q2 | method | 10.1016/j.undsp.2024.04.008 | no |  | 0.2887 | 22.5 | 437 | Junfeng Sun[a] , Yong Fang[a][,][⇑] , Hu Luo[a] , Zhigang Yao[a] , Long Xiang[b] , Jianfeng Wang[a] , Yubo Wang[a] , Yifan Jiang[a] | What method is proposed in this paper? |
| scientific_articles | 109 | 1 | q3 | result | 10.1016/j.undsp.2024.04.008 | no |  | 0.3577 | 27.5 | 140 | Junfeng Sun[a] , Yong Fang[a][,][⇑] , Hu Luo[a] , Zhigang Yao[a] , Long Xiang[b] , Jianfeng Wang[a] , Yubo Wang[a] , Yifan Jiang[a] | What are the main experimental results? |
| scientific_articles | 109 | 3 | q1 | factoid | 10.1016/j.undsp.2024.04.008 | no |  | 0.3144 | 26.6 | 1722 | Junfeng Sun[a] , Yong Fang[a][,][⇑] , Hu Luo[a] , Zhigang Yao[a] , Long Xiang[b] , Jianfeng Wang[a] , Yubo Wang[a] , Yifan Jiang[a] | What is the main contribution of this paper? |
| scientific_articles | 109 | 3 | q2 | method | 10.1016/j.undsp.2024.04.008 | no |  | 0.2806 | 22.6 | 1126 | Junfeng Sun[a] , Yong Fang[a][,][⇑] , Hu Luo[a] , Zhigang Yao[a] , Long Xiang[b] , Jianfeng Wang[a] , Yubo Wang[a] , Yifan Jiang[a] | What method is proposed in this paper? |
| scientific_articles | 109 | 3 | q3 | result | 10.1016/j.undsp.2024.04.008 | no |  | 0.3444 | 20.3 | 414 | Junfeng Sun[a] , Yong Fang[a][,][⇑] , Hu Luo[a] , Zhigang Yao[a] , Long Xiang[b] , Jianfeng Wang[a] , Yubo Wang[a] , Yifan Jiang[a]; Unknown; ScienceDirect | What are the main experimental results? |
| scientific_articles | 109 | 5 | q1 | factoid | 10.1016/j.undsp.2024.04.008 | no |  | 0.2864 | 22.1 | 2674 | Junfeng Sun[a] , Yong Fang[a][,][⇑] , Hu Luo[a] , Zhigang Yao[a] , Long Xiang[b] , Jianfeng Wang[a] , Yubo Wang[a] , Yifan Jiang[a]; ScienceDirect | What is the main contribution of this paper? |
| scientific_articles | 109 | 5 | q2 | method | 10.1016/j.undsp.2024.04.008 | no |  | 0.2694 | 20.3 | 2504 | Junfeng Sun[a] , Yong Fang[a][,][⇑] , Hu Luo[a] , Zhigang Yao[a] , Long Xiang[b] , Jianfeng Wang[a] , Yubo Wang[a] , Yifan Jiang[a] | What method is proposed in this paper? |
| scientific_articles | 109 | 5 | q3 | result | 10.1016/j.undsp.2024.04.008 | yes | 4 | 0.3131 | 21.1 | 1343 | Junfeng Sun[a] , Yong Fang[a][,][⇑] , Hu Luo[a] , Zhigang Yao[a] , Long Xiang[b] , Jianfeng Wang[a] , Yubo Wang[a] , Yifan Jiang[a]; Unknown; ScienceDirect | What are the main experimental results? |
| scientific_articles | 109 | 10 | q1 | factoid | 10.1016/j.undsp.2024.04.008 | no |  | 0.2568 | 20.8 | 4645 | Junfeng Sun[a] , Yong Fang[a][,][⇑] , Hu Luo[a] , Zhigang Yao[a] , Long Xiang[b] , Jianfeng Wang[a] , Yubo Wang[a] , Yifan Jiang[a]; ScienceDirect | What is the main contribution of this paper? |
| scientific_articles | 109 | 10 | q2 | method | 10.1016/j.undsp.2024.04.008 | no |  | 0.2555 | 20.1 | 4622 | Junfeng Sun[a] , Yong Fang[a][,][⇑] , Hu Luo[a] , Zhigang Yao[a] , Long Xiang[b] , Jianfeng Wang[a] , Yubo Wang[a] , Yifan Jiang[a]; ScienceDirect | What method is proposed in this paper? |
| scientific_articles | 109 | 10 | q3 | result | 10.1016/j.undsp.2024.04.008 | yes | 4 | 0.2683 | 19.9 | 4788 | Junfeng Sun[a] , Yong Fang[a][,][⇑] , Hu Luo[a] , Zhigang Yao[a] , Long Xiang[b] , Jianfeng Wang[a] , Yubo Wang[a] , Yifan Jiang[a]; Unknown; ScienceDirect | What are the main experimental results? |
| scientific_articles | 109 | 15 | q1 | factoid | 10.1016/j.undsp.2024.04.008 | no |  | 0.2384 | 20.4 | 7791 | Junfeng Sun[a] , Yong Fang[a][,][⇑] , Hu Luo[a] , Zhigang Yao[a] , Long Xiang[b] , Jianfeng Wang[a] , Yubo Wang[a] , Yifan Jiang[a]; ScienceDirect | What is the main contribution of this paper? |
| scientific_articles | 109 | 15 | q2 | method | 10.1016/j.undsp.2024.04.008 | yes | 14 | 0.2473 | 21.4 | 8810 | Junfeng Sun[a] , Yong Fang[a][,][⇑] , Hu Luo[a] , Zhigang Yao[a] , Long Xiang[b] , Jianfeng Wang[a] , Yubo Wang[a] , Yifan Jiang[a]; ScienceDirect | What method is proposed in this paper? |
| scientific_articles | 109 | 15 | q3 | result | 10.1016/j.undsp.2024.04.008 | yes | 4 | 0.2440 | 21.6 | 8853 | Junfeng Sun[a] , Yong Fang[a][,][⇑] , Hu Luo[a] , Zhigang Yao[a] , Long Xiang[b] , Jianfeng Wang[a] , Yubo Wang[a] , Yifan Jiang[a]; Unknown; ScienceDirect | What are the main experimental results? |
| scientific_articles | 109 | 20 | q1 | factoid | 10.1016/j.undsp.2024.04.008 | no |  | 0.2224 | 20.7 | 10480 | Junfeng Sun[a] , Yong Fang[a][,][⇑] , Hu Luo[a] , Zhigang Yao[a] , Long Xiang[b] , Jianfeng Wang[a] , Yubo Wang[a] , Yifan Jiang[a]; ScienceDirect; Unknown | What is the main contribution of this paper? |
| scientific_articles | 109 | 20 | q2 | method | 10.1016/j.undsp.2024.04.008 | yes | 14 | 0.2407 | 22.8 | 12386 | Junfeng Sun[a] , Yong Fang[a][,][⇑] , Hu Luo[a] , Zhigang Yao[a] , Long Xiang[b] , Jianfeng Wang[a] , Yubo Wang[a] , Yifan Jiang[a]; ScienceDirect | What method is proposed in this paper? |
| scientific_articles | 109 | 20 | q3 | result | 10.1016/j.undsp.2024.04.008 | yes | 4 | 0.2257 | 21.0 | 11674 | Junfeng Sun[a] , Yong Fang[a][,][⇑] , Hu Luo[a] , Zhigang Yao[a] , Long Xiang[b] , Jianfeng Wang[a] , Yubo Wang[a] , Yifan Jiang[a]; Unknown; ScienceDirect | What are the main experimental results? |

