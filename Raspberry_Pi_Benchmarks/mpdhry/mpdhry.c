/*
 cc  mpdhry.c dhry22.c cpuidc.c -lrt -lc -lm -O3 -o MP-DHRY
  #define version "Linux/ARM v1.0"
  gcc mpdhry.c dhry22.c cpuidc.c -lrt -lc -lm -O3 -lpthread -o MP-DHRY
  gcc 4.8
  gcc mpdhry.c dhry22.c cpuidc.c -lrt -lc -lm -O3 -mcpu=cortex-a7 -mfloat-abi=hard -mfpu=neon-vfpv4 -lpthread -o MP-DHRYPiA7
  ./MP-DHRYPiA7
  #define version "Linux/ARM V7A v1.0"

  taskset 0x00000001 ./MP-DHRYPiA7
  
 *************************************************************************
 *
 *                   "DHRYSTONE" Benchmark Program
 *                   -----------------------------
 *
 *  Version:    C, Versi #define version "Linux/ARM V7A v1.0"on 2.1
 *
 *  File:       dhry_1.c (part 2 of 3)
 *
 *  Date:       May 25,  #define version "Linux/ARM V7A v1.0"1988
 *
 *  Author:     Reinhold P. Weicker
 *
 *************************************************************************
*/



 #include <stdio.h>
 #include <stdlib.h>
 #include <string.h>
 #include "dhry.h"
 #include <math.h>
 #include "cpuidh.h"
 #include <time.h> 
 #include <pthread.h> 

// #define version "Linux/ARM v1.0"
 #define version "Linux/ARM V7A v1.0"
 

/* Global Variables: */
 
 Rec_Pointer     Ptr_Glob,
                 Next_Ptr_Glob;
 int             Int_Glob;
 Boolean         Bool_Glob;
 char            Ch_1_Glob,
                 Ch_2_Glob;
 
 char Reg_Define[40] = "Register option      Selected.";
 double  secs;
 double  startSecs;
 char resultchars[1000];


  Enumeration Func_1 (Capital_Letter Ch_1_Par_Val,
                                           Capital_Letter Ch_2_Par_Val);
   /* 
   forward declaration necessary since Enumeration may not simply be int
   */
 
 #ifndef ROPT
 #define REG
         /* REG becomes defined as empty */
         /* i.e. no register variables   */
 #else
 #define REG register
 #endif

 void Proc_1 (REG Rec_Pointer Ptr_Val_Par);
 void Proc_2 (One_Fifty *Int_Par_Ref);
 void Proc_3 (Rec_Pointer *Ptr_Ref_Par);
 void Proc_4 (); 
 void Proc_5 ();
 void Proc_6 (Enumeration Enum_Val_Par, Enumeration *Enum_Ref_Par);
 void Proc_7 (One_Fifty Int_1_Par_Val, One_Fifty Int_2_Par_Val,
                                              One_Fifty *Int_Par_Ref);
 void Proc_8 (Arr_1_Dim Arr_1_Par_Ref, Arr_2_Dim Arr_2_Par_Ref,
                               int Int_1_Par_Val, int Int_2_Par_Val);
                               
 Boolean Func_2 (Str_30 Str_1_Par_Ref, Str_30 Str_2_Par_Ref);

 
 /* variables for time measurement: */
 
 #define Too_Small_Time 2
 
   REG   unsigned int         Number_Of_Runs; 
         int         endit, count;
         int         errors;
         int         nopause = 1;

 pthread_t tid[100]; 
 pthread_attr_t * attrt = NULL; 
 pthread_mutex_t mutext = PTHREAD_MUTEX_INITIALIZER;


void *dhrystones(void *arg)
{

 int             Arr_1_Glob [50];
 int             Arr_2_Glob [50] [50];
 long            thread;

         One_Fifty   Int_1_Loc;
   REG   One_Fifty   Int_2_Loc;
         One_Fifty   Int_3_Loc;
         Enumeration Enum_Loc;
         Str_30      Str_1_Loc;
         Str_30      Str_2_Loc;

   Next_Ptr_Glob = (Rec_Pointer) malloc (sizeof (Rec_Type));
   Ptr_Glob = (Rec_Pointer) malloc (sizeof (Rec_Type));
 
   Ptr_Glob->Ptr_Comp                    = Next_Ptr_Glob;
   Ptr_Glob->Discr                       = Ident_1;
   Ptr_Glob->variant.var_1.Enum_Comp     = Ident_3;
   Ptr_Glob->variant.var_1.Int_Comp      = 40;
   strcpy (Ptr_Glob->variant.var_1.Str_Comp, 
           "DHRYSTONE PROGRAM, SOME STRING");       
   strcpy (Str_1_Loc, "DHRYSTONE PROGRAM, 1'ST STRING");
 
   Arr_2_Glob [8][7] = 10;
         /* Was missing in published program. Without this statement,   */
         /* Arr_2_Glob [8][7] would have an undefined value.            */
         /* Warning: With 16-Bit processors and Number_Of_Runs > 32000, */
         /* overflow may occur for this array element.                  */

   REG   int         Run_Index;
         int         i;
   REG   char        Ch_Index;

       thread = (long)arg;
       Arr_2_Glob [8][7] = 10;          
       for (Run_Index = 1; Run_Index <= Number_Of_Runs; ++Run_Index)
       {
 
         Proc_5();
         Proc_4();
           /* Ch_1_Glob == 'A', Ch_2_Glob == 'B', Bool_Glob == true */
         Int_1_Loc = 2;
         Int_2_Loc = 3;
         strcpy (Str_2_Loc, "DHRYSTONE PROGRAM, 2'ND STRING");
         Enum_Loc = Ident_2;
         Bool_Glob = ! Func_2 (Str_1_Loc, Str_2_Loc);
           /* Bool_Glob == 1 */
         while (Int_1_Loc < Int_2_Loc)  /* loop body executed once */
         {
           Int_3_Loc = 5 * Int_1_Loc - Int_2_Loc;
             /* Int_3_Loc == 7 */
           Proc_7 (Int_1_Loc, Int_2_Loc, &Int_3_Loc);
             /* Int_3_Loc == 7 */
           Int_1_Loc += 1;
         }   /* while */
            /* Int_1_Loc == 3, Int_2_Loc == 3, Int_3_Loc == 7 */
         Proc_8 (Arr_1_Glob, Arr_2_Glob, Int_1_Loc, Int_3_Loc);
           /* Int_Glob == 5 */
         Proc_1 (Ptr_Glob);
         for (Ch_Index = 'A'; Ch_Index <= Ch_2_Glob; ++Ch_Index)
                              /* loop body executed twice */
         {
           if (Enum_Loc == Func_1 (Ch_Index, 'C'))
               /* then, not executed */
             {
               Proc_6 (Ident_1, &Enum_Loc);
               strcpy (Str_2_Loc, "DHRYSTONE PROGRAM, 3'RD STRING");
               Int_2_Loc = Run_Index;
               Int_Glob = Run_Index;
             }
         }
           /* Int_1_Loc == 3, Int_2_Loc == 3, Int_3_Loc == 7 */
         Int_2_Loc = Int_2_Loc * Int_1_Loc;
         Int_1_Loc = Int_2_Loc / Int_3_Loc;
         Int_2_Loc = 7 * (Int_2_Loc - Int_3_Loc) - Int_1_Loc;
           /* Int_1_Loc == 1, Int_2_Loc == 13, Int_3_Loc == 7 */
         Proc_2 (&Int_1_Loc);
           /* Int_1_Loc == 5 */
 
       }   /* loop "for Run_Index" */
       if (Arr_2_Glob[8][7] != Number_Of_Runs + 10) errors = errors + 1;
}

void main()
{
   count = 10;   
   Number_Of_Runs = 5000;
   int     g, threads;
   int     tc;
   long    ii;
   double  User_Time[5];
   double  Vax_Mips[5];
   double  DhryPerSec[5];
   int     threadc[5];
   char    errorMsg[100];

    FILE    *outfile;
    
    outfile = fopen("MP-DHRY.txt","a+");
    if (outfile == NULL)
    {
        printf ("Cannot open results file \n\n");
        printf(" Press Enter\n");
        g  = getchar();
        exit (0);
    }
    printf("\n");
    getDetails();
    local_time();     

    printf(" ##########################################\n"); 
    fprintf (outfile, " #####################################################\n");                     

    //printf ("\nFrom File /proc/cpuinfo\n");
    //printf("%s\n", configdata[0]);
    //printf ("\nFrom File /proc/version\n");
    //printf("%s\n", configdata[1]);

    printf("\n MP-Dhrystone Benchmark %s %s\n", version, timeday);
    printf("     Using 1, 2, 4 and 8 Threads\n\n");
    printf("     Threads  Dhrys/sec   VAX MIPS\n");

    fprintf(outfile, "\n  MP-Dhrystone Benchmark %s %s\n", version, timeday);
    fprintf(outfile, "                    Using 1, 2, 4 and 8 Threads\n\n");

   tc = 1;
   errors = 0;
   for (threads=1; threads<9; threads=threads*2)
   {
       printf("      %4d", threads);
       if (threads == 1)
       {    
           do
           {
        
               Number_Of_Runs = Number_Of_Runs * 2;
               count = count - 1;
               start_time();
                       
               pthread_create(&tid[0], attrt, dhrystones, (void *)0);   
               pthread_join(tid[0], NULL);
                    
               end_time();
               User_Time[tc] = secs;
        
               if (User_Time[tc] > 0.5)
               {
                     count = 0;
               }
               else
               {
                     if (User_Time[tc] < 0.05)
                     {
                          Number_Of_Runs = Number_Of_Runs * 5;
                     }
               }
           } 
           while (count >0);
       }
       else
       {
           start_time();
           for (ii=0; ii<threads; ii++)
           {
               pthread_create(&tid[ii], attrt, dhrystones, (void *)ii);
           }

           for(ii=0;ii<threads;ii++)
           {
              pthread_join(tid[ii], NULL);
           }
           end_time();
           User_Time[tc] = secs;
       }
       threadc[tc] = threads;
       DhryPerSec[tc] = (double) Number_Of_Runs * (double)threads / User_Time[tc];
       Vax_Mips[tc] = DhryPerSec[tc] / 1757.0;
       printf("%13.0f%11.2f\n", DhryPerSec[tc], Vax_Mips[tc]);
       tc = tc + 1;
   }
   if (errors == 0)
   {
       sprintf(errorMsg, " Internal pass count correct all threads");
   }
   else
   {
       sprintf(errorMsg, " Internal pass count %d ERRORS", errors);
   }
   printf("\n %s\n\n", errorMsg);

   fflush(stdout);                
   fflush(outfile);                

   fprintf(outfile, " Threads                %9d%9d%9d%9d\n"
                    " Seconds                %9.2lf%9.2lf%9.2lf%9.2lf\n"
                    " Dhrystones per Second  %9.0lf%9.0lf%9.0lf%9.0lf\n"
                    " VAX MIPS rating        %9.0lf%9.0lf%9.0lf%9.0lf\n\n",
                      threadc[1], threadc[2], threadc[3], threadc[4],
                      User_Time[1], User_Time[2], User_Time[3], User_Time[4],
                      DhryPerSec[1], DhryPerSec[2], DhryPerSec[3], DhryPerSec[4],
                      Vax_Mips[1], Vax_Mips[2], Vax_Mips[3], Vax_Mips[4]); 
   fprintf(outfile, "        %s\n\n", errorMsg);

   local_time();
   printf("   End of test %s\n", timeday);
   fprintf(outfile, "         End of test %s", timeday);        

   fprintf (outfile, "\nSYSTEM INFORMATION\n\nFrom File /proc/cpuinfo\n");
   fprintf (outfile, "%s \n", configdata[0]);
   fprintf (outfile, "\nFrom File /proc/version\n");
   fprintf (outfile, "%s \n", configdata[1]);
   fprintf (outfile, "\n");
   fflush(outfile);                
   //char moredata[1024];
   //printf("Type additional information to include in MP-DHRY.txt - Press Enter\n");
   //if (fgets (moredata, sizeof(moredata), stdin) != NULL)
   //          fprintf (outfile, "Additional information - %s\n", moredata);     fflush(stdout);                
   //fflush(outfile);                
   fclose(outfile);

    return;
 }


 void Proc_1 (REG Rec_Pointer Ptr_Val_Par)
 /******************/
 
     /* executed once */
 {
   REG Rec_Pointer Next_Record = Ptr_Val_Par->Ptr_Comp;  
                                         /* == Ptr_Glob_Next */
   /* Local variable, initialized with Ptr_Val_Par->Ptr_Comp,    */
   /* corresponds to "rename" in Ada, "with" in Pascal           */
   
   structassign (*Ptr_Val_Par->Ptr_Comp, *Ptr_Glob);
   Ptr_Val_Par->variant.var_1.Int_Comp = 5;
   Next_Record->variant.var_1.Int_Comp 
         = Ptr_Val_Par->variant.var_1.Int_Comp;
   Next_Record->Ptr_Comp = Ptr_Val_Par->Ptr_Comp;
   Proc_3 (&Next_Record->Ptr_Comp);
     /* Ptr_Val_Par->Ptr_Comp->Ptr_Comp 
                         == Ptr_Glob->Ptr_Comp */
   if (Next_Record->Discr == Ident_1)
     /* then, executed */
   {
     Next_Record->variant.var_1.Int_Comp = 6;
     Proc_6 (Ptr_Val_Par->variant.var_1.Enum_Comp, 
            &Next_Record->variant.var_1.Enum_Comp);
     Next_Record->Ptr_Comp = Ptr_Glob->Ptr_Comp;
     Proc_7 (Next_Record->variant.var_1.Int_Comp, 10, 
            &Next_Record->variant.var_1.Int_Comp);
   }
   else /* not executed */
     structassign (*Ptr_Val_Par, *Ptr_Val_Par->Ptr_Comp);
 } /* Proc_1 */
 
 
 void Proc_2 (One_Fifty *Int_Par_Ref)
 /******************/
     /* executed once */
     /* *Int_Par_Ref == 1, becomes 4 */
 
 {
   One_Fifty  Int_Loc;
   Enumeration   Enum_Loc;
 
   Int_Loc = *Int_Par_Ref + 10;
   do /* executed once */
     if (Ch_1_Glob == 'A')
       /* then, executed */
     {
       Int_Loc -= 1;
       *Int_Par_Ref = Int_Loc - Int_Glob;
       Enum_Loc = Ident_1;
     } /* if */
   while (Enum_Loc != Ident_1); /* true */
 } /* Proc_2 */
 
 void Proc_3 (Rec_Pointer *Ptr_Ref_Par)
 /******************/
     /* executed once */
     /* Ptr_Ref_Par becomes Ptr_Glob */
 
 {
   if (Ptr_Glob != Null)
     /* then, executed */
     *Ptr_Ref_Par = Ptr_Glob->Ptr_Comp;
   Proc_7 (10, Int_Glob, &Ptr_Glob->variant.var_1.Int_Comp);
 } /* Proc_3 */
 
 
void Proc_4 () /* without parameters */
 /*******/
     /* executed once */
 {
   Boolean Bool_Loc;
 
   Bool_Loc = Ch_1_Glob == 'A';
   Bool_Glob = Bool_Loc | Bool_Glob;
   Ch_2_Glob = 'B';
 } /* Proc_4 */
 
 void Proc_5 () /* without parameters */
 /*******/
     /* executed once */
 {
   Ch_1_Glob = 'A';
   Bool_Glob = false;
 } /* Proc_5 */
 
 
         /* Procedure for the assignment of structures,          */
         /* if the C compiler doesn't support this feature       */
 #ifdef  NOSTRUCTASSIGN
 memcpy (d, s, l)
 register char   *d;
 register char   *s;
 register int    l;
 {
         while (l--) *d++ = *s++;
 }
 #endif



 

