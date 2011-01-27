/*
	parallel object POPCSearchNode 
	This parallel object is in charged of the resources discivery over the grid's node. Each POPCSearchNode is running locally with a JobMgr.

	UPDATES : 
	Author		Date 			Comment

	clementval	2010/04/19	All code added for the semester project begins with this comment //Added by clementval, ends with //End of add
	clementval	2010/04/19	All code modified during the semester project begins with //Modified by clementval, ends with //End of modification
	clementval	2010/04/09	Add method and variable to hold the reference of the associated JobMgr.
	clementval 	2010/05/10	Remove useless constructor and add a constrcutor with challenge string and deamon boolean value. Add an inherotance of the class paroc_service base to transform this parclass
									in a POPC service.
*/

#ifndef _NODE_PH
#define _NODE_PH


#include <time.h>
#include <sys/time.h>

#include <list>
#include <map>
#include "request.h"
#include "response.h"
#include "popc_search_node_info.h"
#include <semaphore.h>

#include "paroc_service_base.ph"
#include "jobmgr.ph"
#include "timer.h"
#include "paroc_thread.h"


#include <iostream>
#include <unistd.h>
#include <stdarg.h>

#define MAXREQTOSAVE 10		// Maximum number of request to save in the history
#define UNLOCK_TIMEOUT 20	//Timeout to unlock the discovery process is no responses are coming

using namespace std;

/*
 *  Class representing POPCSearchNode to discover resource on the grid, inherite from paroc_service_base
 */
parclass POPCSearchNode : virtual public paroc_service_base {

public :
	//Node's constructore 
	POPCSearchNode(const paroc_string &challenge, bool deamon) @{ od.runLocal(true);};
   
	// Destructor
	~POPCSearchNode();
	
	seq sync void setJobMgrAccessPoint(const paroc_accesspoint &jobmgrAccess);
	conc sync paroc_accesspoint getJobMgrAccessPoint();
	seq  sync  void         setPOPCSearchNodeId(paroc_string nodeId);
   conc sync  paroc_string getPOPCSearchNodeId();
   seq  sync  void         setOperatingSystem(paroc_string operatingSys);
   conc sync  paroc_string getOperatingSystem();
	seq  sync  void 			setPower(float p);
	conc sync  float			getPower();
   seq  sync  void         setCpuSpeed(int cpuSpeed);
   conc sync  int          getCpuSpeed();
   seq  sync  void         setMemorySize(float memorySize);
   conc sync  int          getMemorySize();
   seq  sync  void         setNetworkBandwidth(int networkBandwidth);
   conc sync  int          getNetworkBandwidth();
   seq  sync  void         setDiskSpace(int diskSpace);
   conc sync  int          getDiskSpace();
	seq  sync  void			setProtocol(paroc_string prot);
	conc sync  paroc_string getProtocol();
	seq  sync  void			setEncoding(paroc_string enc);
	conc sync  paroc_string getEncoding();

	// Method allowing adding Neighbor to the node
	seq  sync  void         addNeighbor(POPCSearchNode &node);

	// Method allowing removing Neighbor to the node
   seq  sync  void         removeNeighbor(POPCSearchNode &node);


	// Method to remove all neighbors (allowing clean destruction of node)
	seq  sync  void         deleteNeighbors();
        
	// Service's entry point to ressource discovery
	conc sync  POPCSearchNodeInfos   launchDiscovery(Request req, int timeout);        

	// Node's entry point to propagate request
	seq  async void         askResourcesDiscovery(Request req, paroc_accesspoint jobmgr_ac, paroc_accesspoint sender);
        
	// Node's return point to give back the response to the initial node
	conc async void         callbackResult(Response resp);

	conc async void unlockDiscovery();

	classuid(1001);
private :
	char log[200];	//log char
	sem_t *pt_locker;	//semaphor used for null waiting time
	int logicalClock;  		// own request's counter
	POPCSearchNodeInfo nodeInfo;     // node's information
	list<POPCSearchNode *> neighborsList; // node's neighbors list
  	list<paroc_string> knownRequests; // already-asked requests
   map<paroc_string, POPCSearchNodeInfos> actualReq;     // own actual requests
   POPSynchronizer actualReqSyn;  // sync. for actual req.
   // internal method to check if local resources fit the request
   seq sync bool checkResource(Request req);
   // internal method returning a list of neighbors
   conc sync list<paroc_string> getNeighbors();

	struct timeval start, end;	//for test purpose
	
	int popc_node_log(const char *log);	//write log in file

};



#endif
