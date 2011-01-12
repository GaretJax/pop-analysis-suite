#ifndef POPCOBJECT_PH_
#define POPCOBJECT_PH_


parclass POPCobject {
    classuid(1500);
private:
    int count;
    
public:
    POPCobject() @{od.encoding("xdr");};
    ~POPCobject();
    
    mutex sync int get();
};


#endif /*POPCOBJECT_PH_*/
