#! / usr / bin / python
import  sys
import  getopt
importar  os


def  generate_source ( carga útil , init_delay = 2500 , loop_count = - 1 , loop_delay = 5000 , pisca = True ):
	head  =  '' '/ *
* Sketch gerado por duck2spark de Marcus Mengs, também conhecido como MaMe82
*
* /
#include "DigiKeyboard.h"
'' '
	init  =  '' '
void setup ()
{
	// inicializa o pino digital como uma saída.
	pinMode (0, SAÍDA); // LED no modelo B
	pinMode (1, SAÍDA); // LED no modelo A
	DigiKeyboard.delay (% d); // aguarde% d milissegundos antes da primeira execução, para dar tempo de inicialização
}
void loop ()
{
'' '  % ( init_delay , init_delay )

	corpo  =  '' '
	// o código deve ser executado neste loop?
	if (i! = 0) {
		DigiKeyboard.sendKeyStroke (0);
		// analisa o script rawencoder do duckencoder
		para (int i = 0; i <DUCK_LEN; i + = 2)
		{
			chave uint8_t = pgm_read_word_near (duckraw + i);
			uint8_t mod = pgm_read_word_near (duckraw + i + 1);
			if (key == 0) // delay (um atraso> 255 é dividido em uma sequência de atrasos)
			{
				DigiKeyboard.delay (mod);
			}
			else DigiKeyboard.sendKeyStroke (tecla, mod);
		}
		eu--;
		DigiKeyboard.delay (% d); // aguarde% d milissegundos antes da próxima iteração do loop
	}
	else if (piscar)
	{
		digitalWrite (0, ALTO); // liga o LED (HIGH é o nível de tensão)
		digitalWrite (1, ALTO);
		atraso (100); // espere um segundo
		digitalWrite (0, BAIXO); // desligue o LED tornando a tensão BAIXA
		digitalWrite (1, BAIXO);
		atraso (100); // espere um segundo
	}
'' '  % ( loop_delay , loop_delay )

	cauda  =  '' '}
'' '
	l  =  len ( carga útil )
	# carga útil na memória FLASH do digispark
	declare  =  "#define DUCK_LEN"  +  str ( l ) +  " \ n const PROGMEM uint8_t duckraw [DUCK_LEN] = { \ n \ t "
	para  c  no  intervalo ( l  -  1 ):
		declare  + =  str ( hex ( ord ( carga útil [ c ]))) +  ","
	declare  + =  str ( hex ( ord ( carga útil [ l  -  1 ]))) +  " \ n }; \ n int i =% d; // quantas vezes a carga útil deve ser executada (-1 para loop infinito) \ n "  %  loop_count
	se  piscar :
		declare  + =  "bool blink = true; \ n "
	mais :
		declare  + =  "bool blink = false; \ n "

	return  head  +  declare  +  init  +  body  +  tail


def  uso ():
	usagescr  =  '' 'MaMe82 duck2spark 1.0
=======================
Converte a carga útil criada por DuckEncoder em arquivo de origem para DigiSpark Sketch
Uso: python duck2spark -i [file ..] build Sketch do arquivo de carga útil RubberDucky especificado
   ou: python duck2spark -i [arquivo ..] -o [arquivo ..] salvar a fonte do Sketch no arquivo de saída especificado
Argumentos:
   -i [arquivo ..] Arquivo de entrada (Payload codificado com DuckEncoder)
   -o [arquivo ..] Arquivo de saída para Sketch, se omitido, stdout é usado
   -l <count> Contagem de loop (1 = execução única (padrão), -1 = execução sem fim, 3 = 3 execuções etc.)
   -f <millis> Atraso em milissegundos antes da execução inicial da carga (padrão 1000)
   -r <millis> Atraso em milissegundos entre as execuções do loop (padrão 5000)
   -n LED de status não pisca após o término da execução da carga útil
Observação: Para usar DEAD KEYS (fe ^ e `no layout de teclado alemão), um SPACE deve ser
	anexado ao script ducky (por exemplo, "STRING ^ working deadkey").
'' '
	imprimir ( usagescr )


def  main ( argv ):
	ifile  =  ""
	ofile  =  Nenhum
	carga útil  =  Nenhum
	loop_count  =  1
	piscar  =  verdadeiro
	init_delay  =  1000
	loop_delay  =  5000
	tente :
		opta , args  =  getopt . getopt ( argv , "hi: o: l: nf: r:" , [ "ajuda" , "input =" , "output =" , "loopcount =" , "noblink" , "initdelay =" , "repeatdelay =" ])
	exceto  getopt . GetoptError :
		uso ()
		sys . saída ( 2 )
	para  opt , arg  em  opts :
		se  optar  por ( "-h" , "--help" ):
			uso ()
			sys . sair ()
		elif  opt  ==  '-d' :
			global  _debug
			_debug  =  1
		elif  opt  in ( "-i" , "--input" ):
			ifile  =  arg
			se  não  os . caminho . isfile ( ifile ) ou  não  os . acesso ( ifile , os . R_OK ):
				print ( "Arquivo de entrada"  +  ifile  +  "não existe ou não é legível" )
				sys . saída ( 2 )
			com  aberto ( ifile , "rb" ) como  f :
				carga útil  =  f . ler ()
		elif  opt  in ( "-o" , "--output" ):
			ofile  =  arg
		elif  opt  in ( "-l" , "--loopcount" ):
			loop_count  =  int ( arg )
		elif  opt  in ( "-f" , "--initdelay" ):
			init_delay  =  int ( arg )
		elif  opt  in ( "-r" , "--repeatdelay" ):
			loop_delay  =  int ( arg )
		elif  opt  in ( "-n" , "--noblink" ):
			blink  =  False
	se a  carga útil  for  Nenhum :
		print ( "Você deve fornecer uma carga gerada por DuckEncoder (opção -i)" )
		sys . saída ( 2 )

	# gerar código-fonte para Sketch
	result  =  generate_source ( carga útil , init_delay = init_delay , loop_count = loop_count , loop_delay = loop_delay , blink = blink )

	se  ofile  for  Nenhum :
		# imprimir para stdout
		imprimir ( resultado )
	mais :
		# escrever para ofile
		com  aberto ( ofile , "w" ) como  f :
			f . escrever ( resultado )


if  __name__  ==  "__main__" :
	se  len ( sys . argv ) <  2 :
		uso ()
		sys . sair ()
	principal ( sys . argv [ 1 :])
