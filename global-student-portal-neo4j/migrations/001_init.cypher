// Clean start (optional)
MATCH (n) DETACH DELETE n;

// Nodes (components)
UNWIND [
  "Global DNS / Geo Routing",
  "CDN + WAF",
  "API Gateway",
  "Identity & SSO",
  "Tenant Config Service",
  "User & RBAC Service",
  "Academic Records Service",
  "Schedule & Attendance Service",
  "Documents & Certificates Service",
  "Notifications Service",
  "Integration Hub",
  "Event Bus",
  "PostgreSQL",
  "Redis Cache",
  "Object Storage",
  "Analytics DB",
  "Institution Systems"
] AS name
CREATE (:Component {name: name});

// Helper: create dependency
// (A)-[:DEPENDS_ON]->(B)

MATCH (dns:Component {name:"Global DNS / Geo Routing"})
MATCH (cdn:Component {name:"CDN + WAF"})
CREATE (dns)-[:DEPENDS_ON]->(cdn);

MATCH (cdn:Component {name:"CDN + WAF"})
MATCH (gw:Component {name:"API Gateway"})
CREATE (cdn)-[:DEPENDS_ON]->(gw);

MATCH (gw:Component {name:"API Gateway"})
MATCH (auth:Component {name:"Identity & SSO"})
CREATE (gw)-[:DEPENDS_ON]->(auth);

// Gateway -> core services
UNWIND [
  "Tenant Config Service",
  "User & RBAC Service",
  "Academic Records Service",
  "Schedule & Attendance Service",
  "Documents & Certificates Service",
  "Notifications Service"
] AS svcName
MATCH (gw:Component {name:"API Gateway"})
MATCH (svc:Component {name:svcName})
CREATE (gw)-[:DEPENDS_ON]->(svc);

// Core -> data stores
MATCH (tenant:Component {name:"Tenant Config Service"})
MATCH (pg:Component {name:"PostgreSQL"})
CREATE (tenant)-[:DEPENDS_ON]->(pg);

MATCH (user:Component {name:"User & RBAC Service"})
MATCH (pg:Component {name:"PostgreSQL"})
MATCH (redis:Component {name:"Redis Cache"})
CREATE (user)-[:DEPENDS_ON]->(pg);
CREATE (user)-[:DEPENDS_ON]->(redis);

MATCH (acad:Component {name:"Academic Records Service"})
MATCH (pg:Component {name:"PostgreSQL"})
CREATE (acad)-[:DEPENDS_ON]->(pg);

MATCH (sched:Component {name:"Schedule & Attendance Service"})
MATCH (pg:Component {name:"PostgreSQL"})
CREATE (sched)-[:DEPENDS_ON]->(pg);

MATCH (docs:Component {name:"Documents & Certificates Service"})
MATCH (pg:Component {name:"PostgreSQL"})
MATCH (obj:Component {name:"Object Storage"})
CREATE (docs)-[:DEPENDS_ON]->(pg);
CREATE (docs)-[:DEPENDS_ON]->(obj);

MATCH (notif:Component {name:"Notifications Service"})
MATCH (redis:Component {name:"Redis Cache"})
CREATE (notif)-[:DEPENDS_ON]->(redis);

// Event bus connections
MATCH (bus:Component {name:"Event Bus"})
MATCH (notif:Component {name:"Notifications Service"})
CREATE (notif)-[:DEPENDS_ON]->(bus);

MATCH (acad:Component {name:"Academic Records Service"})
MATCH (bus:Component {name:"Event Bus"})
CREATE (acad)-[:DEPENDS_ON]->(bus);

MATCH (sched:Component {name:"Schedule & Attendance Service"})
MATCH (bus:Component {name:"Event Bus"})
CREATE (sched)-[:DEPENDS_ON]->(bus);

MATCH (docs:Component {name:"Documents & Certificates Service"})
MATCH (bus:Component {name:"Event Bus"})
CREATE (docs)-[:DEPENDS_ON]->(bus);

// Integration hub
MATCH (hub:Component {name:"Integration Hub"})
MATCH (bus:Component {name:"Event Bus"})
MATCH (inst:Component {name:"Institution Systems"})
CREATE (hub)-[:DEPENDS_ON]->(bus);
CREATE (hub)-[:DEPENDS_ON]->(inst);

// Analytics pipeline
MATCH (bus:Component {name:"Event Bus"})
MATCH (adb:Component {name:"Analytics DB"})
CREATE (bus)-[:DEPENDS_ON]->(adb);