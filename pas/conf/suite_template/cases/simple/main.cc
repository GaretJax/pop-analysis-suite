#include "simple.ph"

#define OBJCOUNT 10

int main(int argc, char** argv) {
    
    POPCobject o;
    
    for (int i = 0; i < OBJCOUNT; i++) {
        printf("The value is: %d\n", o.get());
    }
    
    return 0;
}
