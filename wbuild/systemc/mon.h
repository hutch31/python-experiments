#include "systemc.h"
#include <stdlib.h>

SC_MODULE(mon)
{
  sc_in<bool> Clk, A, B, F;

  void Monitor()
  {
    sc_time t;
    t = sc_time_stamp();
    printf("%8llu A=%d B=%d F=%d\n", t.value(), int(A), int(B), int(F));
  }

  SC_CTOR(mon)
  {
    SC_METHOD(Monitor);
    sensitive << Clk.pos();
  }
};
