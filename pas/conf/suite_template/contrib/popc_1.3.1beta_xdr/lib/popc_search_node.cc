/* 
UPDATES : 
Authors		Date			Comment
clementval	2010/04/19	All code added for the semester project begins with this comment //Added by clementval, ends with //End of add
clementval	2010/04/19	All code modified during the semester project begins with //Modified by clementval, ends with //End of modification
clementval 	2010/05/05	Remove useless constructor.
clementval	2010/05/15	Add a funcionnality of null waiting (timer + semaphor)
clementval	2010/05/19	Rename the Node parclass in POPSearchNode
*/
#include "popc_search_node.ph"


//Delcaration of a small timer thread for POPSearchNode parclass
class NodeThread : public paroc_thread {
public:
	NodeThread(int timeout, const paroc_accesspoint &node);
	virtual void start();
	virtual void stop();
private:
	int _timeout;
	bool _running;
	bool _unlock;
	paroc_accesspoint _node;
};

//Implementation of this small class
NodeThread::NodeThread(int timeout, const paroc_accesspoint &node) : paroc_thread(true) {
	_timeout = timeout;
	_node = node;
	_running = true;
	_unlock = true;
}
//Start a timer and contact de POPCSearchNode when it's finished
void NodeThread::start(){
	POPCSearchNode n(_node);
	Timer t;
	t.Start();
	while(_running){
		usleep(100000);
		if(t.Elapsed() > _timeout){
			t.Stop();
			_running = false;
		}
	}
	if(_unlock)
		n.unlockDiscovery();
}
//Stop the timer
void NodeThread::stop(){
	_unlock = false;
	_running = false;
}

//POPCSearchNode's constructor with challenge string (necessary to stop the object) and deamon boolean value to put the object in a deamon mode
POPCSearchNode::POPCSearchNode(const paroc_string &challenge, bool deamon) : paroc_service_base(challenge) {
	popc_node_log("NODE Created ...");
	logicalClock=0;
	sem_t locker;
	pt_locker = &locker;
	if(deamon) Start();
}

//POPCSearchNode's destructor
POPCSearchNode::~POPCSearchNode(){
	popc_node_log("POPCSearchNode destroyed ...");
}


// Set the ID of the POPCSearchNode
void POPCSearchNode::setPOPCSearchNodeId(paroc_string nodeId){
	nodeInfo.nodeId = nodeId;
	sprintf(log, "POPCSearchNode id : %s", nodeInfo.nodeId.GetString());
	popc_node_log(log);
}

// Get the ID of this POPCSearchNode
paroc_string POPCSearchNode::getPOPCSearchNodeId(){
    return nodeInfo.nodeId;
}

// Set the operating system
void POPCSearchNode::setOperatingSystem(paroc_string operatingSystem){
    nodeInfo.operatingSystem = operatingSystem;
}

// Get the operating system
paroc_string POPCSearchNode::getOperatingSystem(){
    return nodeInfo.operatingSystem;
}

//Set the compute power
void POPCSearchNode::setPower(float p){
    nodeInfo.power = p;
}

//Get the compute power
float POPCSearchNode::getPower(){
    return nodeInfo.power;
}

// Set the CPU Speed
void POPCSearchNode::setCpuSpeed(int cpuSpeed){
    nodeInfo.cpuSpeed = cpuSpeed;
}

// Get the CPU Speed
int POPCSearchNode::getCpuSpeed(){
    return nodeInfo.cpuSpeed;
}

// Set the memory size
void POPCSearchNode::setMemorySize(float memorySize){
    nodeInfo.memorySize = memorySize;
}

// Get the memory size
int POPCSearchNode::getMemorySize(){
    return nodeInfo.memorySize;
}

// Set the network bandwidth
void POPCSearchNode::setNetworkBandwidth(int networkBandwidth){
    nodeInfo.networkBandwidth = networkBandwidth;
}

// Get the network bandwidth
int POPCSearchNode::getNetworkBandwidth(){
    return nodeInfo.networkBandwidth;
}

// Set the disk space
void POPCSearchNode::setDiskSpace(int diskSpace){
    nodeInfo.diskSpace = diskSpace;
}

// Get the disk space
int POPCSearchNode::getDiskSpace(){
    return nodeInfo.diskSpace;
}

//Set the protocol
void POPCSearchNode::setProtocol(paroc_string prot){
    nodeInfo.protocol = prot;
}

//Get the protocol
paroc_string POPCSearchNode::getProtocol(){
    return nodeInfo.protocol;
}

//Set the encoding
void POPCSearchNode::setEncoding(paroc_string enc){
    nodeInfo.encoding = enc;
}

//Get the encoding
paroc_string POPCSearchNode::getEncoding(){
    return nodeInfo.encoding;
}


// Add a POPCSearchNode as a neighbor of this POPCSearchNode
void POPCSearchNode::addNeighbor(POPCSearchNode &node){
	sprintf(log, "NODE_ADD;%s", node.GetAccessPoint().GetAccessString());
	popc_node_log(log);
	neighborsList.push_back(new POPCSearchNode(node));
}

// Remove a POPCSearchNode as a neighbor of this POPCSearchNode
void POPCSearchNode::removeNeighbor(POPCSearchNode &node){
	sprintf(log, "NODE_REMOVE;%s", node.GetAccessPoint().GetAccessString());
	popc_node_log(log);
	list<POPCSearchNode *>::iterator i;
	for(i=neighborsList.begin(); i != neighborsList.end(); i++){
		paroc_accesspoint crt = (*i)->GetAccessPoint();
		if(strcmp(crt.GetAccessString(), node.GetAccessPoint().GetAccessString()) == 0){
			neighborsList.erase(i);
			break;
		}
	}	
}


// Remove current POPCSearchNode's neighbors. Used after resources discovery to delete
// properly the parallel objects
void POPCSearchNode::deleteNeighbors(){
	list<POPCSearchNode *>::iterator i;
	for(i=neighborsList.begin(); i != neighborsList.end(); i++)
		delete (*i);
	neighborsList.clear();
}

// Called from the timer to unlock the semaphor used when the waiting time is set to 0
void POPCSearchNode::unlockDiscovery(){
	sem_post(pt_locker);
}

// Service's entry point for resources discovery. This method will return an
// object of type "POPCSearchNodeInfos" containing information about nodes which fit the
// request
POPCSearchNodeInfos POPCSearchNode::launchDiscovery(Request req, int timeout){
	gettimeofday(&start, NULL);	//This line is just for test purpose so it can be removed in production release

	
	sprintf(log, "LDISCOVERY;TIMEOUT;%d", timeout);
	popc_node_log(log);
	// create a new unique request id with the name of the node and its
	// logical clock. This uniqueId is added to the request
	char uId[MAXREQUNIQUEIDLENGTH];
	sprintf(uId,"%s__%d", getPOPCSearchNodeId().GetString(), logicalClock);
	req.setUniqueId(uId);
	logicalClock++;
    
    // "network" self-reference to current node for callback results
    // prepare results place for current request in the currently running
    // request's list.
    POPCSearchNodeInfos nInfos;
    actualReqSyn.lock();
    actualReq[req.getUniqueId()] = nInfos;
    actualReqSyn.unlock();
    
    // begin resources discovery locally
    askResourcesDiscovery(req, GetAccessPoint(), GetAccessPoint());
    // wait until timeout

	if(timeout == 0){
		sem_init(pt_locker, 0, 0);
		NodeThread *timer = new NodeThread(UNLOCK_TIMEOUT, GetAccessPoint());
		timer->create();
		sem_wait(pt_locker);
		timer->stop();
		popc_node_log("Unlocker timer started ...");
	} else {
		sleep(timeout);
	}
    
    // getting results for current request and construct of POPCSearchNodeInfos object
    actualReqSyn.lock();
    
    POPCSearchNodeInfos results;
    map<paroc_string, POPCSearchNodeInfos>::iterator i;
    
    // ! for-statement because of problem with map comparison and paroc_string !
    for(i=actualReq.begin(); i != actualReq.end(); i++){
        paroc_string id = (*i).first;
        if(strcmp(id.GetString(), req.getUniqueId().GetString()) == 0){
            results = i->second;
            break;
        }
    }
	// erase the place for this request disallowing adding more results for this
   // request in the future
   actualReq.erase(req.getUniqueId());
   actualReqSyn.unlock();
	sprintf(log, "RESULTS;%d", results.getNodeInfos().size());
	popc_node_log(log);
   return results;
}

// POPCSearchNode's entry point to propagate request in the grid
// asker is the node which will receive positiv result
void POPCSearchNode::askResourcesDiscovery(Request req, paroc_accesspoint node_ap, paroc_accesspoint sender){

	//Should be removed in production release
/*	char *sleepm;
	int sleepmint;
	if(sleepm=getenv("POPC_SEARCHSLEEPMACHINE")){
		sleepmint = atoi(sleepm);
		if(sleepmint > 1000) sleepmint = 1000;
		sleepmint = sleepmint * 1000;
		usleep(sleepmint);
		popc_node_log("WAIT_MACHINE");
	}
*/
	//End of should be removed

	sprintf(log, "ASKRDISCOVERY;ASKER;%s;REQID;%s", node_ap.GetAccessString(), req.getUniqueId().GetString());
	popc_node_log(log);
   // check if the request has already been asked
   list<paroc_string>::iterator k;
   for(k = knownRequests.begin(); k != knownRequests.end(); k++){
      if(strcmp(k->GetString(),req.getUniqueId().GetString()) == 0){
			sprintf(log, "ALREADY_ASKED_REQUEST;%s", req.getUniqueId().GetString());
			popc_node_log(log);
			POPCSearchNode nsender(sender);
			JobMgr jsender(nsender.getJobMgrAccessPoint());
			jsender.UnregisterNode(GetAccessPoint());
			removeNeighbor(nsender);			
         return;
      }
   }
   // save current request's uniqueId in the history
   knownRequests.push_back(req.getUniqueId());
   
   // check the maximum length of the history
   if(knownRequests.size() > MAXREQTOSAVE){
       knownRequests.pop_front();
   }
    
   // save the received exploration list
   ExplorationList oldEL(req.getExplorationList());
   
   // Adding the node's neighbors in the exploration list
   req.addNodeToExplorationList(getPOPCSearchNodeId(), getNeighbors());

   // Check local resources
   bool isResourcesOk = checkResource(req);
	sprintf(log, "CHECK;%s", (isResourcesOk)?"OK":"FAILED");      
	popc_node_log(log);
   if(isResourcesOk){
        	// If local resources are OK, build the response and give it back to
        	// 'asker' node
        	Response* resp = new Response(req.getUniqueId(),
                                      POPCSearchNodeInfo(nodeInfo), 
                                      req.getExplorationList());
			POPCSearchNode asker(node_ap);
			sprintf(log, "SEND_REP;DEST;%s", node_ap.GetAccessString());
			popc_node_log(log);
      	asker.callbackResult(*resp);
        	// delete resp;
    }
    
    // Continue the propagation if more hops are allowed. It continues if the
    // max hops is zero to avoid counting "initial node" discovery.
	if(req.getMaxHops() == 0){
		sprintf(log, "PROPAGATION_STOP_HOP;%d", req.getMaxHops());
		popc_node_log(log);
	}else  {
		sprintf(log, "HOPS;%d", req.getMaxHops());
		popc_node_log(log);
	}

	//Should be removed in production release
/*	char *sleepn;
	int sleepnint;
	if(sleepn=getenv("POPC_SEARCHSLEEPNETWORK")){
		sleepnint = atoi(sleepn);
		if(sleepnint > 1000) sleepnint = 1000;
		sleepnint = sleepnint * 1000;
		usleep(sleepnint);
		popc_node_log("WAIT_NETWORK");
	}
*/
	//End of should be removed

	if(req.getMaxHops() >= 0 || req.getMaxHops() == UNLIMITED_HOPS){
      list<POPCSearchNode *>::iterator i;
      // check if the local neighbors are already asked with the originally 
      // received exploration list
      for(i = neighborsList.begin(); i != neighborsList.end(); i++){
         if(!oldEL.isIn((*i)->getPOPCSearchNodeId())){
				paroc_string nid;
				nid = (*i)->getPOPCSearchNodeId();
				sprintf(log, "FORWARD;DEST;%s", nid.GetString());
				popc_node_log(log);
         	(*i)->askResourcesDiscovery(req, node_ap, GetAccessPoint());
         }
      }
   }
}

// POPCSearchNode's return point to give back the response to the initial node
void POPCSearchNode::callbackResult(Response resp){
	//Just for test purpose, must be removed in production release
	gettimeofday(&end, NULL);
	long msec_start;
	msec_start = (start.tv_sec)*1000000;
	msec_start += (start.tv_usec);
	long msec_end;
	msec_end = (end.tv_sec)*1000000;
	msec_end += (end.tv_usec);
	long diff = msec_end-msec_start;
	POPCSearchNodeInfo dni = resp.getFoundNodeInfo();
	sprintf(log, "RESP;REQID;%s;SENDER;%s;TIME;START;%ld;END;%ld;DIFF;%ld", resp.getReqUniqueId().GetString() , dni.nodeId.GetString(), msec_start, msec_end, diff);
	popc_node_log(log);
	//End for test
   actualReqSyn.lock();
   map<paroc_string, POPCSearchNodeInfos>::iterator i;

    // visit the currently running list
    for(i=actualReq.begin(); i != actualReq.end(); i++){
        paroc_string id = (*i).first;
        // if the request's uniqueId is present, add the response to the list
        // and break the for-statement.
        if(strcmp(id.GetString(), resp.getReqUniqueId().GetString()) == 0){
            i->second.addANodeInfo(resp.getFoundNodeInfo());
            break;
        }
    }
    actualReqSyn.unlock();
	sem_post(pt_locker);
}

// internal comparison between request and local resources
bool POPCSearchNode::checkResource(Request req){    
    // check about the operating system
    if(req.hasOperatingSystemSet()){
       //Should be check if the current architecture is in the list of requested architecture by the request
    }
 
   // check about the minimal cpu speed
	if(req.hasMinCpuSpeedSet()){
		//popc_node_log("MINCPUSPEED %d, %d", req.getMinCpuSpeed(), getCpuSpeed());      
      if(req.getMinCpuSpeed() > getCpuSpeed())
          return false;
   }

	
   // check about the exact cpu speed
   if(req.hasExpectedCpuSpeedSet()){
	//	popc_node_log("EXPCPUSPEED %d, %d", req.getExpectedCpuSpeed(), getCpuSpeed());      
      if(req.getExpectedCpuSpeed() <= getCpuSpeed())
          return false;
   }


	
    // check about the minimal memory size
    if(req.hasMinMemorySizeSet()){
		//	popc_node_log("MINMEM %d, %d", req.getMinMemorySize(), getMemorySize());      
      	if(req.getMinMemorySize() > getMemorySize())
         	return false;
    }


   // check about the exact memory size
   if(req.hasExpectedMemorySizeSet()){
	//	popc_node_log("EXPMEM %d, %d", req.getExpectedMemorySize(), getMemorySize());      
      if(req.getExpectedMemorySize() <= getMemorySize())
          return false;
   }
   
  
    // check about the minimal network bandwith
	if(req.hasMinNetworkBandwidthSet()){
	//	popc_node_log("MINBAN %d, %d", req.getMinNetworkBandwidth(), getNetworkBandwidth());      
     	if(req.getMinNetworkBandwidth() > getNetworkBandwidth())
     		return false;
   }
   
   // check about the exact network bandwith
   if(req.hasExpectedNetworkBandwidthSet()){
	//	popc_node_log("EXPBAN %d, %d", req.getExpectedNetworkBandwidth(), getNetworkBandwidth());      
		if(req.getExpectedNetworkBandwidth() <= getNetworkBandwidth())
			return false;
	}

	// check about the minimal disk space
	if(req.hasMinDiskSpaceSet()){
	//	popc_node_log("MINDIS %d, %d", req.getMinDiskSpace(), getDiskSpace());      
		if(req.getMinDiskSpace() > getDiskSpace())
			return false;
	}
 
    // check about the min power
	if(req.hasMinPowerSet()){
	//	popc_node_log("MINPOW %f, %f", req.getMinPower(), getPower());      
		if(req.getMinPower() > getPower())
	   	return false;
	}

	if(req.hasExpectedPowerSet()){
	//	popc_node_log("EXPPOW %f, %f", req.getExpectedPower(), getPower());      
		if(req.getExpectedPower() > getPower())
	   	return false;
	}
    
    // if no return until there, everything's OK!
    return true;
}

// Return a list of neighbors' nodeId
list<paroc_string> POPCSearchNode::getNeighbors(){
    list<paroc_string> neighbors;
    list<POPCSearchNode *>::iterator i;
    for(i = neighborsList.begin(); i != neighborsList.end(); i++){
        neighbors.push_back((*i)->getPOPCSearchNodeId());
    }
    return neighbors;
}

//Set the associated JobMgr access point
void POPCSearchNode::setJobMgrAccessPoint(const paroc_accesspoint &jobmgrAccess){
	nodeInfo.jobmgr = jobmgrAccess;
}

//return the associated JobMgr access point
paroc_accesspoint POPCSearchNode::getJobMgrAccessPoint(){
	return nodeInfo.jobmgr;
}

//Method to write log in a file
int POPCSearchNode::popc_node_log(const char *log)
{
	char *tmp=getenv("POPC_TEMP");
	char logfile[256];
	if (tmp!=NULL) sprintf(logfile,"%s/popc_node_log",tmp);
	else strcpy(logfile, "/tmp/pop_node.log");

	FILE *f=fopen(logfile,"a");
	if (f==NULL) return 1;
	time_t t=time(NULL);
	fprintf(f, ctime(&t));
	/*va_list ap;
	va_start(ap, log);
	vfprintf(f, log, ap);*/
	fprintf(f,log);
	fprintf(f,"\n");
	//va_end(ap);
	fclose(f);
	return 0;
}
