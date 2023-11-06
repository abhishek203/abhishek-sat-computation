from multiprocessing import Process
import time

def p(i):
    time.sleep(2)
    print(i)
    time.sleep(2)

def main():
    for i in range(10):
        # time.sleep(2)
        # Process(target=p,args=(i,)).start()
        p(i)
        
        
if __name__ == "__main__":

    s = time.time()

    # main()
    px = Process(target=main)
    px.start()
    px.join()

    print(f"TT : {time.time() - s}")