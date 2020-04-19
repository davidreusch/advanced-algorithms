#include <stdio.h>
#include <inttypes.h>
#include <math.h>
#include <time.h>
#include <stdlib.h>

#define NUM_MULTS 1000000


uint32_t power(uint32_t a, uint32_t n)
{
    uint32_t res = 1;
    for (uint32_t i = 0; i < n; i++)
    {
        res *= a;
    }
    return  res;
}

uint32_t karatsuba(uint32_t a, uint32_t b, uint32_t l) 
{
    if (l < 2 ) {
        return a * b;
    }

    //assume l is a power of two
    uint32_t l_half = l / 2;

    //shift low values out right and retain high values
    uint32_t a_h = a >> (l_half);
    uint32_t b_h = b >> (l_half);

    //clear upper bits to the left and shift back 
    uint32_t leftshift = 32 - l_half;
    uint32_t a_l = (a << leftshift) >> (leftshift);
    uint32_t b_l = (b << leftshift) >> (leftshift);

    //printf("l: %d\na: %d, a_h : %d, a_l: %d, b: %d, b_h: %d, b_l: %d\n", l, a, a_h, a_l, b, b_h, b_l);


    uint32_t high_term = karatsuba(a_h, b_h, l_half);
    uint32_t low_term = karatsuba(a_l, b_l, l_half);
    uint32_t middle_term = karatsuba(a_h + a_l, b_h + b_l, l_half ) -  high_term - low_term;

    return ((high_term << l) + (middle_term << l_half)) + low_term;
}

int get_max_bits(uint32_t a, uint32_t b) 
{
    //das ist evtl. viel aufwendiger als einfach pauschal
    //Größe 32 zu nehmen
    int bits_a = floor(log(a) / log(2)) + 1;
    int bits_b = floor(log(b) / log(2)) + 1;

    //nächste Registerbreite = 2 ^ (ceil( log2(bits_a)))
    int power_a = ceil(log(bits_a) / log(2));
    int power_b = ceil(log(bits_b) / log(2));

    int l = power_a > power_b ? power(2, power_a) : power(2, power_b);
    
    return l;
/*
    //find out number of bits in a
    uint32_t save_a = a;
    uint32_t count_a = 0;
    while (a > 0) 
    {
        a >>= 1;
        count_a++;
    }

    //find out number of bits in b
    uint32_t save_b = b;
    uint32_t count_b = 0;
    while (b > 0) 
    {
        b >>= 1;
        count_b++;
    }

    //get max number of bits in a and b
    uint32_t bigger = count_a > count_b ? count_a : count_b;

    //get registersize (2^4, 2^8, 2^16, 2^32) for numbers
    uint32_t i;
    uint32_t l = 1;
    for (i = 1; i <= 5; i++) 
    {
        l *= 2;
        
        if (l >= bigger) 
        {
            break;
        }
    }
    printf("l for numbers %d, %d: %d\n", save_a, save_b, l);

    //call karatsuba with right registersize
    return karatsuba(save_a, save_b, l);
*/
}




uint32_t naive_mult(uint32_t a, uint32_t b) 
{
    uint32_t res = 0;

    while (b != 0) 
    {
        if (b % 2 == 1) 
        {
            res += a;
        }
        a <<= 1;
        b >>= 1;
    }

    return res;

}

double avg(double array[], int len) 
{
    double akk = 0;
    for (int i = 0; i < len; i++) 
    {
        akk += array[i];
    }
    return akk / len;

}

double measure_kara(int repetitions) 
{

 //   double times[repetitions];
    srand(time(NULL));

    clock_t begin = clock();
    for (int i = 0; i < repetitions; i++) 
    {
        uint32_t a = (uint32_t) (rand() % 0x010000 + 0x010000) ;
        uint32_t b = (uint32_t) (rand() % 0x010000 + 0x010000) ;
        
        //int l = get_max_bits(a,b);
       

        uint32_t result = karatsuba(a,b,32);

        if (result != a * b) 
        {
            printf("Falsches Resultat bei Kara Mult: %u * %u = %u, richtiges resultat: %u", a, b, result, a * b);
            break;
        }


//        times[i] = time_kara;

    }
    clock_t end = clock();
    double time_kara = ((double)end - (double)begin) / CLOCKS_PER_SEC;

    //return avg(times, repetitions);
    //
    return time_kara;

}

double measure_naive_bin(int repetitions) 
{

    srand(time(NULL));

    clock_t begin = clock();
    for (int i = 0; i < repetitions; i++) 
    {
        
        uint32_t a = (uint32_t) (rand() % 0x01000000 + 0x01000000) ;
        uint32_t b = (uint32_t) (rand() % 0x01000000 + 0x01000000) ;

        uint32_t result = naive_mult(a,b);
        if (result != a * b) 
        {
            printf("Falsches Resultat bei naiver Mult: %u * %u = %u, richtiges resultat: %u", a, b, result, a * b);
            break;
        }

    }
    clock_t end = clock();
    double time = ((double)end - (double)begin) / CLOCKS_PER_SEC;

    return time;

}




int main(int argc, char* argv[]) 
{
    int a = 128919; 
    int b = 934892;

    printf("karatsuba: %d, richtig: %d\n", karatsuba(a,b,32), a * b); 
    double time_kara = measure_kara(NUM_MULTS);
    printf("karatsuba: %f seconds for %d multiplications  \n", time_kara, NUM_MULTS);

    double time_naive = measure_naive_bin(NUM_MULTS);
    printf("naive mult: %f seconds for  %d multiplications \n",time_naive, NUM_MULTS);


    return 0;

}

