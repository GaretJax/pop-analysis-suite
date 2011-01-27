#ifndef _INTEGER_PH
#define _INTEGER_PH

parclass Integer
{
	classuid(1000);

public:	
	Integer(int maxhop, int timeout) @{ od.search(maxhop, 0, timeout);};
	Integer() @{ od.search(10, 200,0); };
	~Integer();

	seq async void Set(int val);
	conc int Get();
	mutex void Add(Integer &other);

private:
	int data;

};

#endif
