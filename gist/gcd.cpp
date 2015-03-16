

// c++/java stein 算法 
int gcd(int a,int b){
    if(a<b)
    {
        //arrange so that a>b 
        int temp = a;
        a = b;
        b=temp;
    } 

    if(0==b)//the base case 
        return a; 

    if(a%2==0 && b%2 ==0)//a and b are even 
        return 2*gcd(a/2,b/2); 

    if ( a%2 == 0)// only a is even 
        return gcd(a/2,b); 

    if ( b%2==0 )// only b is even 
        return gcd(a,b/2); 

    return gcd((a+b)/2,(a-b)/2);// a and b are odd 

} 
