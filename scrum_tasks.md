### Dataset Preparation

1. **Design the dataset structure:** 5 points
2. **Create dataset generation:** 5 points
3. **Tweak dataset factors:** 3 points

### System Design and Setup

4. **Design system architecture:** 8 points

### Orchestrator Service

5. **Design Orchestrator Service Architecture:** 5 points
6. **Implement Event Generation (Order):** 4 points
7. **Implement Event Generation (Failure):** 4 points
8. **Setup Redis Queues:** 3 points
9. **Integrate Event Generation with Redis Queues:** 5 points
10. **Move Orchestrator to Docker:** 2 points

### PostgreSQL Service

11. **Setup PostgreSQL Database:** 3 points
12. **Design PostgreSQL Service Architecture:** 5 points
13. **Create the database schema:** 5 points
14. **Create the data ingestion logic:** 5 points
15. **Implement Order Event Processing in PostgreSQL:** 5 points
16. **Implement Failure Event Processing in PostgreSQL:** 5 points
17. **Record Query Processing Time in PostgreSQL:** 3 points
18. **Send Metrics to Metrics Queue from PostgreSQL:** 3 points
19. **Move PostgreSQL service and PostgreSQL to Docker:** 2 points

### Neo4j Service

20. **Setup Neo4j Database:** 3 points
21. **Design Neo4j Service Architecture:** 5 points
22. **Create the data ingestion logic:** 5 points
23. **Create fast ingest logic:** 5 points
24. **Implement Order Event Processing in Neo4j:** 5 points
25. **Implement Failure Event Processing in Neo4j:** 5 points
26. **Record Query Processing Time in Neo4j:** 3 points
27. **Send Metrics to Metrics Queue from Neo4j:** 3 points
28. **Move Neo4j service and Neo4j to Docker:** 2 points

### Metrics Collection

29. **Design Metrics Queues:** 5 points
30. **Implement Metrics Collection Logic:** 5 points

### Analyzer Service

31. **Design Analyzer Service Architecture:** 5 points
32. **Implement Metrics Analysis Logic:** 5 points
33. **Compute Total Processing Time for Each Database:** 3 points
34. **Generate Comparative Analysis Reports:** 3 points
35. **Move Analyzer Service to Docker:** 2 points

### Animator Service

36. **Design Animator Service Architecture:** 5 points
37. **Implement Data Visualization:** 5 points
38. **Setup Flask server:** 3 points
39. **Implement Data Visualization endpoint:** 5 points
40. **Move Animator Service to Docker:** 2 points

### Final Integration and Testing

41. **Design Docker Compose:** 8 points
42. **Time and define dependencies:** 6 points
43. **Create setup scripts:** 5 points
44. **Write README:** 3 points
45. **Test the system to ensure it is solid:** 5 points
46. **Test the system on a new machine:** 5 points
