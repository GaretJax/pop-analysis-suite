#include "simple.ph"


POPCobject::POPCobject() {
    count = 0;
}

POPCobject::~POPCobject() {}

int POPCobject::get() {
    return count++;
}


@pack(POPCobject);
