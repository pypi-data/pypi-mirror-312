class PolynomialOperations:
  def __init__(self):
    pass
  # 1-create a polynomial with the given list of coefficients.
  def polynomial(self,l):
    n=len(l)
    string=''
    for i in range(n):
      tempans=''
      if(l[i]!=1 or i==n-1):
         tempans+=f"{str(l[i])}"
      if(n-i-1==1):
        tempans+="x+"
      elif(n-i-1!=0):
        tempans+=f"x^{n-i-1}+"
      string+=tempans
    return string
  
# 2-Returns the degree of the polynomial
  def degreeOfPolyomial(self,l):
    return len(l)-1
  
  def truncateZeroes(self,l):
    for i in range(len(l)):
        if l[i]!=0:
          l=l[i:]
          return l
    return []
  
  def add_polynomials(self,l,m):
    # Reverse both lists to align terms by increasing degree
    l = l[::-1]
    m = m[::-1]
    
    # Determine the length of the result list
    max_len = max(len(l), len(m))
    
    l.extend([0] * (max_len - len(l)))
    m.extend([0] * (max_len - len(m)))
    
    # Add corresponding coefficients
    result = [l[i] + m[i] for i in range(max_len)]
    
    # Reverse the result to put the highest degree at the 0th index
    return result[::-1]
  
  # l-m
  def subtract_polynomials(self,l,m):
    # Reverse both lists to align terms by increasing degree
    l = l[::-1]
    m = m[::-1]
    
    # Determine the length of the result list
    max_len = max(len(l), len(m))
    
    l.extend([0] * (max_len - len(l)))
    m.extend([0] * (max_len - len(m)))
    
    # Add corresponding coefficients
    result = [l[i] - m[i] for i in range(max_len)]
    
    # Reverse the result to put the highest degree at the 0th index
    result=result[::-1]
    result=self.truncateZeroes(result)
    return result

# multiplying a polynomial by a scalar quantity
  def scalarMultiply_Polynomial(self,l,c):
    return [c*i for i in l]

  def multiply_Polynomial(self,l,m):
    len1=len(l)
    len2=len(m)
    ans=[0 for i in range(len1+len2-1)]

    for i in range(len1):
      for j in range(len2):
        ans[i+j] += l[i]*m[j]
        # print(ans)
    ans=self.truncateZeroes(ans)
    return ans 

    # divide the leading term of dividend by the leading term of the divisor
    # in this way u will get the quotient
    # multiply the entore divisor with this quotient.
    # subtract it from the dividend
    # repeat until the degree of dividend  is less than divisor

  # m-->dividend
  # l--->divisor
  def divide_Polynomial(self,m,l):
    l=self.truncateZeroes(l)
    m=self.truncateZeroes(m)
    if(len(l)==0 or len(m)==0):return "Division not possible"
    # if (all(x == 0 for x in l) or all(x == 0 for x in m)):
    #       return -1
    if(len(l)==1):
      # i.e divisor has only one element definitely constant hi hoga
      l=self.scalarMultiply_Polynomial(m,1/l[0])
      return [l,[0]]
    # Higher Degree Divisor
    if(len(l)>len(m)):return [[0],m]

    ans=[0 for i in range(len(m)-len(l)+1)]
    while(self.degreeOfPolyomial(l)<=self.degreeOfPolyomial(m) and all(i!=0 for i in m)):
      quotient_degree=len(m)-len(l)
      quotient=m[0]/l[0]
      ans[quotient_degree]=(quotient)
      # construct a list from the quotient obtained
      q=[quotient if(i==quotient_degree) else 0 for i in range(quotient_degree,-1,-1)]
      
      # print(m,l)

      mul_list=self.multiply_Polynomial(q,l)
      sub_list=self.subtract_polynomials(m,mul_list)
      
      m=sub_list
    return [ans[::-1],sub_list]  

  def evaluate_polynomial(self,coefficients, x):
      result = 0
     
      for coefficient in coefficients:
          result = result * x + coefficient
      return result
  
  # polynomial derivative and integration-indefinite
  # nth derivatives of a polynomial 
  def polynomial_derivative(self,coeff,n):
    try:
      if(n<0):
        raise ValueError
      if(n==0):
        # 0th order derivative
        return coeff
      if(n>=len(coeff)):
        # //degree of the coeff is less than the order of the differentiation
        return [0]
      count=0
      while(count<n):
        new_coeff=[coeff[i]*(len(coeff)-i-1) for i in range(len(coeff)-1)]
        count+=1
        coeff=new_coeff
      return coeff
    except ValueError:
       print("Cannot do negative order differential.")

  def polynomial_integration(self,coeff,const=0):
    new_coeff=[coeff[i]/(len(coeff)-i) if(coeff[i]!=0) else 0 for i in range(len(coeff))]
    new_coeff.append(const)
    return new_coeff

