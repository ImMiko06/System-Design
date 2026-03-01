// fanOut = out-degree (DEPENDS_ON)
// fanIn  = in-degree  (others depend on this)
// Instability I = fanOut / (fanIn + fanOut)

MATCH (c:Component)
OPTIONAL MATCH (c)-[o:DEPENDS_ON]->(:Component)
WITH c, count(o) AS fanOut
OPTIONAL MATCH (:Component)-[i:DEPENDS_ON]->(c)
WITH c, fanOut, count(i) AS fanIn
WITH c, fanIn, fanOut,
     CASE WHEN (fanIn + fanOut) = 0
          THEN 0.0
          ELSE toFloat(fanOut) / toFloat(fanIn + fanOut)
     END AS instability
SET c.fanIn = fanIn,
    c.fanOut = fanOut,
    c.instability = instability
RETURN c.name AS component, fanIn, fanOut, instability
ORDER BY instability DESC, fanOut DESC;

MATCH (c:Component)
RETURN
"| Component | Fan-in | Fan-out | Instability (I) |" AS line
UNION ALL
MATCH (c:Component)
RETURN
"| " + c.name + " | " + toString(coalesce(c.fanIn,0)) + " | " + toString(coalesce(c.fanOut,0)) +
" | " + toString(round(coalesce(c.instability,0.0)*1000)/1000.0) + " |" AS line
ORDER BY line;