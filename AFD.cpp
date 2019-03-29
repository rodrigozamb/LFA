#include<bits/stdc++.h>
#include <fstream>
using namespace std;

typedef struct transicao{
    int q0,qf;
    char a;
}Transicao;


int main(){

    string line;
    ifstream myfile ("fonte.txt");
    
    

    if (myfile.is_open())
    {
        int a;
        myfile>>a;
        bool estados[a];

        for(int i=0;i<a;i++)estados[i]=false;
        getline(myfile,line);
        vector<string> v{explode(line, ' ')};
        for(int i=0;i<v.size();i++)cout<<v[i]<<endl;
        vector<Transicao> transicoes;



        /*while ( getline (myfile,line) )
        {
            if(line!="")cout << line << '\n';
        }
        */
        
        
        myfile.close();
    }else cout << "Unable to open file"<<endl; 

    return 0;
}