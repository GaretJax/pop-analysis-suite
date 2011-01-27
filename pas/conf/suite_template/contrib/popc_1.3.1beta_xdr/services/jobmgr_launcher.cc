/*
UPDATES : 
Authors		Date			Comment
clementval	2010/04/19	All code added for the semester project begin with this comment 	//Added by clementval
clementval	2010/04/19	All code modified during the semester project begins with //Modified by 								clementval, ends with //End of modification
clementval	2010/05/10	Creating a POPCSearchNode befor creating the JobMgr, change the JobMgr 		creation by passing the POPCSearchNode access point
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#ifdef POPC_GLOBUS
#include "jobmgr_globus.ph"
#else
#include "jobmgr.ph"
#endif
//Added by clementval
//Header file for the parclass POPCSearchNode
#include "popc_search_node.ph"
//End of add

void Usage()
{
	printf("Usage: jobmgr_launcher [-servicepoint=<host>[:port]] [-port=<port>] <start [options]> | <stop>\n\tOptions:\n\t  [-code=<jobmgr code file>] [-conf=<jobmgr config file>] [-challenge=<string>] [-genchallenge=<out file>] [-proxy=<proxy contact>] [-test]\n");
	exit(1);
}

int main(int argc, char **argv)
{
	int port;
	char url[256],url1[256];
	paroc_string host;
	paroc_string conf;
	paroc_string objcode;
	paroc_string challenge;
	char str[1024];

	char *tmp;
	bool stop=(paroc_utils::checkremove(&argc,&argv,"stop")!=NULL);
	if (!stop && paroc_utils::checkremove(&argc,&argv,"start")==NULL) Usage();

	if ((tmp=paroc_utils::checkremove(&argc,&argv,"-servicepoint="))==NULL)
	{
		tmp=paroc_utils::checkremove(&argc,&argv,"-port=");
		if (tmp==NULL) sprintf(str,"%s:2711",(const char *)paroc_system::GetHost());
		else sprintf(str,"%s:%s",(const char *)paroc_system::GetHost(),tmp);
	}
	else
	{
		strcpy(str,tmp);
		if (strchr(str,':')==NULL) strcat(str,":2711");
	}
	host=str;

	tmp=paroc_utils::checkremove(&argc,&argv,"-challenge=");
	if (tmp!=NULL) challenge=tmp;
	else if ((tmp=paroc_utils::checkremove(&argc,&argv,"-genchallenge="))!=NULL && !stop)
	{

		srand(time(NULL));
		char tmpstr[256];
		for (int i=0;i<255;i++) tmpstr[i]=(char)('A'+23.0*rand()/(RAND_MAX+1.0) );
		tmpstr[255]=0;
		challenge=tmpstr;
		int fd=creat(tmp,O_CREAT | S_IRUSR | S_IWUSR);
		if (fd<0)
		{
			perror("Challenge output file");
			return 1;
		}
		if (write(fd,tmpstr,255)!=255)
		{
			perror("Error on writing challenge string");
			return 1;
		}
		close(fd);
	}

	try
	{
		if (stop)
		{
			paroc_accesspoint pt;
			pt.SetAccessString(host);
			fprintf(stderr,"Connecting to %s....\n", (const char *)host);
			JobMgr mgr(pt);
			//Added by clementval
			//Calling the Stop method of the POPCSearchNode to destroyed the object
			POPCSearchNode n(mgr.GetNodeAccessPoint());
			if (!n.Stop(challenge)){
				fprintf(stderr, "Bad challenge string. Can not stop the service...\n");
				return 1;
			}
			fprintf(stderr,"POPCSearchNode stopped\n");
			//End of add
			if (!mgr.Stop(challenge))
			{
				fprintf(stderr, "Bad challenge string. Can not stop the service...\n");
				return 1;
			}
			fprintf(stderr,"JobMgr stopped\n");
			return 0;
		}

		if ((tmp=paroc_utils::checkremove(&argc,&argv,"-conf="))==NULL && (tmp=getenv("JOBMGR_CONF"))==NULL)
		{
			char *paroc_location=getenv("POPC_LOCATION");
			if (paroc_location==NULL)
			{
				fprintf(stderr,"ERROR: POPC_LOCATION environment variable is not set.\n");
				Usage();
			}

#ifdef POPC_GLOBUS
			sprintf(str,"%s/etc/jobmgr.globus.conf",paroc_location);
#else
			sprintf(str,"%s/etc/jobmgr.conf",paroc_location);
#endif
			conf=str;

		} else conf=tmp;

		bool daemon=(paroc_utils::checkremove(&argc,&argv,"-test")==NULL);

		//Added by clementval
		POPCSearchNode n(challenge, daemon);
		printf("POPCSearchNode access point: %s\n", n.GetAccessPoint().GetAccessString());
		//End of add
#ifdef POPC_GLOBUS
		GlobusJobMgr info(daemon, conf,challenge, host);
#else
		//Modified by clementval
		//Add the POPCSearchNode accesspoint as a parameter
		JobMgr info(daemon, conf, challenge, host, n.GetAccessPoint());
		//End of modification
#endif
		if (!daemon) printf("JobMgr access point: %s\n",info.GetAccessPoint().GetAccessString());
		if (daemon)
		{
			printf("%s",info.GetAccessPoint().GetAccessString());
			return 0;
		}
		//Testing....
		printf("Get Info:\n");
		char type[64];
		char str[256];
		while (1)
		{
			printf("Information type:\n");
			if (scanf("%s",type)!=1) break;
			try
			{
				paroc_string typestr(type), val;
				if (info.Query(typestr,val))
				{
					printf("%s: \tType=%s\tValue=%s\n",info.GetAccessPoint().GetAccessString(), type, (const char *)val);
				}
				else
				{
					printf("%s: \tValue not found\n",info.GetAccessPoint().GetAccessString());
				}
			}
			catch (paroc_exception *e)
			{
				errno=e->Code();
				paroc_system::perror("Invoke exception occurs\n");
				delete e;
			}
		}
	}
	catch (paroc_exception *e)
	{
		errno=e->Code();
		paroc_system::perror("Exception occurs\n");
		delete e;
		return 1;
	}
	return 0;
}
