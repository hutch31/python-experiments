#include "systemc.h"
#include "nand.h"
#include "mon.h"
#include <stdlib.h>
#include "Vvnand.h"

//#include "foo_stim.h"

SC_MODULE(stim)
{
  sc_out<bool> A, B;
  sc_in<bool> Clk;

  void StimGen()
  {
    A.write(false);
    B.write(false);
    wait();
    A.write(false);
    B.write(true);
    wait();
    A.write(true);
    B.write(false);
    wait();
    A.write(true);
    B.write(true);
    wait();
    printf("DEBUG: stopping sim\n");
    sc_stop();
  }
  SC_CTOR(stim)
  {
    SC_THREAD(StimGen);
    sensitive << Clk.pos();
  }
};


int sc_main(int argc, char* argv[])
{
  sc_signal<bool> ASig, BSig, FSig;
  sc_clock TestClk("TestClock", 10, SC_NS, 0.5, 1, SC_NS);

  //sc_set_default_time_unit(1, SC_NS);
  stim Stim1("Stimulus");
  Stim1.A(ASig);
  Stim1.B(BSig);
  Stim1.Clk(TestClk);

/*
  nand2 DUT("nand2");
  DUT.A(ASig);
  DUT.B(BSig);
  DUT.F(FSig);
  */
  Vvnand DUT("nand2");
  DUT.A(ASig);
  DUT.B(BSig);
  DUT.F(FSig);

  mon Monitor1("Monitor");
  Monitor1.A(ASig);
  Monitor1.B(BSig);
  Monitor1.F(FSig);
  Monitor1.Clk(TestClk);

  sc_start();  // run forever

  return 0;

}
