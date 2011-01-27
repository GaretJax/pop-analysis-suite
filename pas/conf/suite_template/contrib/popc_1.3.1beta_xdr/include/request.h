/* 
UPDATES : 
Authors		Date			Comment
clementval	2010/04/19	All code added for the semester project begins with this comment //Added by clementval, ends with //End of add
clementval	2010/04/19	All code modified during the semester project begins with //Modified by clementval, ends with //End of modification

*/

#ifndef _REQUEST_H
#define _REQUEST_H
#include "explorationList.h"
#include "../include/paroc_string.h"
#include "../include/paroc_base.h"

#define MAXREQUNIQUEIDLENGTH 50    // Maximum length of uniqueId of a request
#define UNLIMITED_HOPS -20         // Fixed value indicating unlimited hops

using namespace std;

/*
 *  Class representing a request of resource discovery. This class must
 *  inherit from POPBase to be passed in the network.
 */ 
class Request : public POPBase{
    public :
        // default constructor without information on the request
        Request();
        
        // constructor with all information
        Request(int maxHops,
                paroc_string nodeId,
                paroc_string operatingSystem, 
                int minCpuSpeed,
                int expectedCpuSpeed,
                float minMemorySize,
                float expectedMemorySize,
                int minNetworkBandwidth,
                int expectedNetworkBandwidth,
                int minDiskSpace,
                int expectedDiskSpace,
		float minPower,
		float expectedPower,
		paroc_string protocol,
        	paroc_string encoding);
                
        // Destructor
        ~Request();

        // Inherited method to serialize the object
        virtual void Serialize(POPBuffer &buf, bool pack);

        // Getters, setters and havers for different information
        void         setUniqueId(paroc_string uniqueId);
        paroc_string getUniqueId();
        
        void         setMaxHops(int maxHops);
        int          getMaxHops();
        
        void         setNodeId(paroc_string nodeId);
        paroc_string getNodeId();
        bool         hasNodeIdSet();
        
        void         setOperatingSystem(paroc_string operatingSystem);
        paroc_string getOperatingSystem();
        bool         hasOperatingSystemSet();
        
        void         setMinCpuSpeed(int cpuSpeed);
        int          getMinCpuSpeed();
        bool         hasMinCpuSpeedSet();
        
        void         setExpectedCpuSpeed(int cpuSpeed);
        int          getExpectedCpuSpeed();
        bool         hasExpectedCpuSpeedSet();
        
        void         setMinMemorySize(float memorySize);
        float        getMinMemorySize();
        bool         hasMinMemorySizeSet();
        
        void         setExpectedMemorySize(float memorySize);
        float        getExpectedMemorySize();
        bool         hasExpectedMemorySizeSet();
        
        void         setMinNetworkBandwidth(float networkBandwidth);
        float        getMinNetworkBandwidth();
        bool         hasMinNetworkBandwidthSet();
        
        void         setExpectedNetworkBandwidth(float networkBandwidth);
        float        getExpectedNetworkBandwidth();
        bool         hasExpectedNetworkBandwidthSet();
        
        void         setMinDiskSpace(int diskSpace);
        int          getMinDiskSpace();
        bool         hasMinDiskSpaceSet();
        
        void         setExpectedDiskSpace(int diskSpace);
        int          getExpectedDiskSpace();
        bool         hasExpectedDiskSpaceSet();

	void 	     setExpectedPower(float power);
	float	     getExpectedPower();
	bool 	     hasExpectedPowerSet();

	void 	     setMinPower(float power);
	float	     getMinPower();
	bool 	     hasMinPowerSet();

	void 	     setProtocol(paroc_string power);
	paroc_string getProtocol();
	bool 	     hasProtocolSet();

	void 	     setEncoding(paroc_string power);
	paroc_string getEncoding();
	bool 	     hasEncodingSet();

	
		
        
        // method allowing adding nodes to the exploration list of the request
        void         addNodeToExplorationList(paroc_string nodeId,
                                              list<paroc_string> neighbors);

        // return the exploration list of the request
        ExplorationList getExplorationList();
        
        // method telling if a node (identified by its name) is present in the
        // exploration list of the request
        bool            isInExplorationList(paroc_string nodeId);

    private :
        paroc_string    _uniqueId;  // unique identifier of the request
        int             _maxHops;   // maximum number of hops for this request

        // request parameters
        paroc_string    _nodeId;
        bool            _hasNodeIdSet;
        paroc_string    _operatingSystem;
        bool            _hasOperatingSystemSet;
        int             _minCpuSpeed;
        bool            _hasMinCpuSpeedSet;
        int             _expectedCpuSpeed;
        bool            _hasExpectedCpuSpeedSet;
        float           _minMemorySize;
        bool            _hasMinMemorySizeSet;
        float           _expectedMemorySize;
        bool            _hasExpectedMemorySizeSet;
        int             _minNetworkBandwidth;
        bool            _hasMinNetworkBandwidthSet;
        int             _expectedNetworkBandwidth;
        bool            _hasExpectedNetworkBandwidthSet;
        int             _minDiskSpace;
        bool            _hasMinDiskSpaceSet;
        int             _expectedDiskSpace;
        bool            _hasExpectedDiskSpaceSet;
	float		_expectedPower;
	bool 		_hasExpectedPowerSet;
	float		_minPower;
	bool 		_hasMinPowerSet;
	paroc_string	_protocol;
	bool		_hasProtocolSet;
	paroc_string	_encoding;
	bool		_hasEncodingSet;
        
        ExplorationList explorationList;    // exploration list of the request
        
        // initiator of the request
        void init();
};

#endif
