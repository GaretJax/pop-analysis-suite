AUTOMAKE_OPTIONS=no-dependencies

CXX=@top_srcdir@/parser/popcc

POPC_FLAGS=-parocdir=@top_srcdir@ -popcpp=@top_srcdir@/parser/popcpp -cxx=@CXX@ -D_PLUGINDIR=\"$(libdir)/plugins\" -D_POPC_RUNTIME_

if LINUX
AM_CXXFLAGS= -D_LINUX $(POPC_FLAGS)
else
AM_CXXFLAGS= $(POPC_FLAGS)
endif

paroc_infmain.%.o: paroc_infmain.%.cc
	$(CXX) -cxxmain $(POPC_FLAGS) $(CXXFLAGS) -DPIC -fPIC -c $< -o $@
paroc_objmain.%.o: paroc_objmain.%.cc
	$(CXX) -cxxmain $(POPC_FLAGS) $(CXXFLAGS) -DPIC -fPIC -c $< -o $@

%.ph.stub_client.o : %.ph
	$(CXX) -cxxmain $(POPC_FLAGS) $(CXXFLAGS) -parclass-nobroker -c $< -o $@

%.ph.stub.o : %.ph
	$(CXX) -cxxmain $(POPC_FLAGS) $(CXXFLAGS) -c $< -o $@

%.ph.stub_client.lo : %.ph
	$(LIBTOOL) --mode=compile --tag=CXX $(CXX) -cxxmain $(POPC_FLAGS) $(CXXFLAGS) -parclass-nobroker -c $< -o $@

%.ph.stub.lo : %.ph
	$(LIBTOOL) --mode=compile --tag=CXX $(CXX) -cxxmain $(POPC_FLAGS) $(CXXFLAGS) -c $< -o $@

lib_LTLIBRARIES = libparoc_common.la  libparoc_service_common.la
#lib_LTLIBRARIES = libparoc_plugin.la

bin_PROGRAMS= testplugin alloctest combox_client combox_server combox_test

libparoc_common_la_SOURCES=system.cc mutex.cc thread.cc string.cc od.cc event.cc buffer.cc buffer_utils.cc combox.cc  \
	broker.cc broker_receive.cc broker_serve.cc object.cc interface.cc allocobj.cc timer.cc accesspoint.cc memspool.cc \
	utils.cc debug.cc exception.cc benchmark.cc combox_factory.cc \
	combox.cc combox_socket.cc buffer_xdr.cc \
	buffer_factory.cc buffer_factory_finder.cc buffer_xdr_factory.cc\
	buffer_raw.cc buffer_raw_factory.cc broker_factory.cc\
	response.cc request.cc explorationList.cc popc_search_node_info.cc
	
libparoc_common_la_LIBADD=paroc_service_base.ph.stub_client.lo popc_search_node.ph.stub_client.lo codemgr.ph.stub_client.lo \
remotelog.ph.stub_client.lo objectmonitor.ph.stub_client.lo appservice.ph.stub_client.lo batchmgr.ph.stub_client.lo
libparoc_common_la_LDFLAGS=-static
libparoc_common_la_CPPFLAGS=

libparoc_service_common_la_SOURCES=service_base.cc jobmgr.cc popc_search_node.cc codemgr.cc remotelog.cc objectmonitor.cc appservice.cc batchmgr.cc
libparoc_service_common_la_LIBADD=paroc_service_base.ph.stub.lo jobmgr.ph.stub.lo popc_search_node.ph.stub.lo codemgr.ph.stub.lo \
remotelog.ph.stub.lo  objectmonitor.ph.stub.lo appservice.ph.stub.lo batchmgr.ph.stub.lo 
libparoc_service_common_la_LDFLAGS=-static -version-info 1:2:0

main_DATA= paroc_objmain.std.o paroc_infmain.std.o
maindir=@libdir@


#paroc_objmain_std.o: paroc_objmain_std.cc
#	$(CXX) -cxxmain $(POPC_FLAGS) $(CXXFLAGS) -DPIC -fPIC -c $< -o $@

testplugin_SOURCES=testplugin.cc 
testplugin_LDFLAGS=-paroc-nolib -L./ -lparoc_common 
testplugin_LDADD=paroc_infmain.std.o
testplugin_CXXFLAGS=$(AM_CXXFLAGS) -DPIC -fPIC


alloctest_SOURCES=alloctest.cc 
alloctest_LDFLAGS=-paroc-nolib -L./ -lparoc_service_common -lparoc_common
alloctest_LDADD=paroc_infmain.std.o
alloctest_CXXFLAGS=$(AM_CXXFLAGS) -DPIC -fPIC

combox_client_SOURCES=combox_client.cc 
combox_client_LDFLAGS=-paroc-nolib -L./ -lparoc_common 
combox_client_LDADD=paroc_infmain.std.o
combox_client_CXXFLAGS=$(AM_CXXFLAGS) -DPIC -fPIC

combox_server_SOURCES=combox_server.cc 
combox_server_LDFLAGS=-paroc-nolib -L./ -lparoc_common 
combox_server_LDADD=paroc_infmain.std.o
combox_server_CXXFLAGS=$(AM_CXXFLAGS) -DPIC -fPIC

combox_test_SOURCES=combox_test.cc 
combox_test_LDFLAGS=-paroc-nolib -L./ -lparoc_common 
combox_test_LDADD=paroc_infmain.std.o
combox_test_CXXFLAGS=$(AM_CXXFLAGS) -DPIC -fPIC



EXTRA_DIST=paroc_infmain.std.cc paroc_objmain.std.cc appservice.ph  popc_search_node.ph codemgr.ph  jobmgr.ph  objectmonitor.ph  paroc_service_base.ph   remotelog.ph batchmgr.ph  

inst_HEADERS=paroc_service_base.ph appservice.ph popc_search_node.ph codemgr.ph remotelog.ph objectmonitor.ph batchmgr.ph jobmgr.ph 
instdir=@includedir@

CLEANFILES=_paroc_*.cc _paroc_*.ph
