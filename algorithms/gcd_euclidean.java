// find greatest common divisor by the Euclidean algorithm
// from http://en.wikipedia.org/wiki/Greatest_common_divisor#Using_Euclid.27s_algorithm
int gcd(int a, int b)
{
	if(a == 0)
	{
		return b;
	}
	else if(b == 0)
	{
		return a;
	}
	else
	{
		int maxValue = Math.max(a, b);
		int minValue = Math.min(a, b);
		
		return gcd(minValue, maxValue % minValue);
	}
}
