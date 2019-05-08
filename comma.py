def comma (integer):
        
    number = list(str(int(float(integer))))
    
    number_of_commas = (len(number)//3) if len(number)%3 != 0 else (len(number)//3)-1
    comma_indices    = [-3]
    [comma_indices.append(comma_indices[-1]-4) for i in range(number_of_commas-1)]
    
    [number.insert(i, ',') for i in comma_indices if len(number)>3]
    
    answer = number[0]
    for i in range(1,len(number)):
        temp = answer
        answer  = answer + number[i]

    return answer