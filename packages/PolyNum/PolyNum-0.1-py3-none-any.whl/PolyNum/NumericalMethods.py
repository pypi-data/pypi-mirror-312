class NumericalMethods:
 
  # calculating the roots of a given polynomial
  def bisection(self,x0,x1,e,func):  
    f=eval(f"lambda x:{func}")
    y0,y1=f(x0),f(x1)
    i=0
    if(y0*y1>0):
      # they are of same signs
      print("Starting values are unsuitable")
      return
    while(abs((x1-x0)/x1)>e):
      x2=(x0+x1)/2
      y2=f(x2)
      i+=1
      if(y0*y2<0):
        x1=x2
      else:
        x0=x2
    # return [x2,f(x2),i]  
    return [x2,i]
    
  def regula_Falsi(self,x0,x1,e,func,n):
    f=eval(f"lambda x:{func}")
    y0,y1=f(x0),f(x1)
    for i in range(n):
      x2=(x0*y1-x1*y0)/(y1-y0)
      y2=f(x2)
      if abs(y2)<=e:
        return [x2,i]
      if(y2*y1<0):
        x1,y1=x2,y2
      else:
        x0,y0=x2,y2

    return [x2,n]

  def newton_raphson(self,x0,e,n,func,diffFunc):
    
    f=eval(f"lambda x:{func}")
    diffF=eval(f"lambda x:{diffFunc}")
    
    for i in range(n):
      y0=f(x0)
      y_0=diffF(x0)
      x1=x0-(y0/y_0)
      if(abs((x1-x0)/x1)<e):
        return [x1,i]
      x0=x1
    return [x0,n] 

  # numerical method of integration
  # trapezoidal rule
  # Approximate the integral of a function f from a to b using the trapezoidal rule with n intervals.

  def trapezoidal_rule(self,f, a, b, n):
    
    f=eval(f"lambda x:{f}")
    h = (b - a) / n
    integral = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        integral += f(a + i * h)
    integral *= h
    return integral

  def simpsons1By3_rule(self,f, a, b, n):
    
    f=eval(f"lambda x:{f}")

    if n % 2 != 0:
        raise ValueError("Number of intervals 'n' must be even for Simpson's 1/3 rule.")

    h = (b - a) / n
    integral = f(a) + f(b)

    for i in range(1, n):
        if i % 2 == 0:
            integral += 2 * f(a + i * h)
        else:
            integral += 4 * f(a + i * h)

    integral *= h / 3
    return integral

  # this will give the value correct upto a tolerance
  def trapezoidal_rule_refined(self,f, a, b, tolerance=1e-6):
    
    f = eval(f"lambda x: {f}")
    # Initial number of intervals
    n = 1
    h = (b - a) / n
    integral_old = 0.5 * h * (f(a) + f(b))  # Initial trapezoidal approximation with n=1
    integral_new=0
    while True:
        n *= 2
        h = (b - a) / n
        
        # Calculate trapezoidal sum with refined intervals
        integral_new = 0.5 * integral_old
        for i in range(1,n,2):
          integral_new+=f(a+i*h)*h

        # print(integral_old,integral_new)
        
        # Check for convergence
        if abs(integral_new - integral_old) < tolerance:
          # print("Number of iterations taken:",n)
          return integral_new
        
        # Update for the next refinement
        integral_old = integral_new

  def simpsons_rule_refined(self,f, a, b, tolerance=1e-6): 
    f = eval(f"lambda x: {f}")
    # Initial number of intervals
    n=2
    h=(b-a)/2
    S1,S2=f(a)+f(b),0
    S4=f(a+h)
    I0,In=0,(S1+4*S4+2*S2)*h/3
    x=0
    # print(I0,In)
    while(True):
      S2,S4=S2+S4,0
      x=a+h/2
      for _ in range(n):
        S4=S4+f(x)
        x=x+h
      h/=2
      n*=2
      I0,In=In,(S1+4*S4+2*S2)*h/3
      # print(I0,In)
      if abs (In-I0) < tolerance:
        # print("The number of iterations taken are:",n/2)
        return In
      
  def gauss_quadrature(self,f, a, b, n=5):
      
      f = eval(f"lambda x: {f}")
      # Gauss points and weights are already known for different quadrature
      if n==5:
          points = [-0.90618, 0.90618,0, 0.538469,-0.538469]
          weights = [0.236927,0.236927, 0.568889, 0.478629,0.478629]
      elif n==4:
          points = [-0.339981,0.339981,-0.861136,0.861136]
          weights = [0.652145,0.652145,0.347855, 0.347855]
      elif n == 3:
          points = [-0.7745966692, 0, 0.7745966692]
          weights = [5/9, 8/9, 5/9]
      elif n == 2:
          points = [-1 / 3**0.5, 1 / 3**0.5]
          weights = [1, 1]
      else:
          raise ValueError("Not supported.")

      # Change of variables
      p = (a + b) / 2
      q = (b - a) / 2

      # Calculate the integral
      integral = 0
      for i in range(n):
          # Transform point to [a, b]
          x = p+q*points[i]
          integral += weights[i] * f(x)

      # Scale by the half range
      integral *= q
      return integral

  # solution of system of linear equations.
  # direct method
  def gaussian_elimination(self,matrix, b):
      n = len(matrix)  # Number of equations
      # augmented matrix
      for i in range(n):
          matrix[i].append(b[i])

      for i in range(n):
          max_row = i
          for k in range(i + 1, n):
              if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                  max_row = k
          # Swap rows if needed
          if matrix[max_row][i] == 0:
              return "No unique solution exists (system is either inconsistent or has infinite solutions)."
          matrix[i], matrix[max_row] = matrix[max_row], matrix[i]

          # Step 2: Making the pivot element 1 
          pivot = matrix[i][i]
          for j in range(i, n + 1):
              matrix[i][j] /= pivot  # Making pivot 1

          for k in range(i + 1, n):
              factor = matrix[k][i]
              for j in range(i, n + 1):
                  matrix[k][j] -= factor * matrix[i][j]

      # Backward Substitution process
      solution = [0] * n
      for i in range(n - 1, -1, -1):
          solution[i] = matrix[i][n]  # Start with the constant term from the augmented matrix
          for j in range(i + 1, n):
              solution[i] -= matrix[i][j] * solution[j]

      return solution

  # iterative method
  def gauss_seidel(self,matrix, b, initial_guess=None, tolerance=1e-10, max_iterations=100):
      
      n = len(matrix)

      if initial_guess is None:
          x = [0.0 for _ in range(n)]
      else:
          x = initial_guess[::]

      for _ in range(max_iterations):
          # Make a copy of the current solution to calculate the next iteration
          x_new = x[::]

          for i in range(n):
              sum_ = sum(matrix[i][j] * x_new[j] for j in range(n) if j != i)

              if matrix[i][i] == 0:
                  return "Diagonal element cannot be zero, adjust matrix for diagonal dominance."
              x_new[i] = (b[i] - sum_) / matrix[i][i]

          # Check for convergence (stop if the difference is within the tolerance for all x values)
          if all(abs(x_new[i] - x[i]) < tolerance for i in range(n)):
              return x_new

          # Update x with x_new for the next iteration
          x = x_new

      # If the method did not converge within the maximum number of iterations
      return "The method did not converge within the maximum number of iterations."

  # Lagrange's interpolation to interpolate the value of a given x onthe basis of the set ofthe given function values
  def lagrange_interpolation(self,x_values, y_values, x):
    
      if len(x_values) != len(y_values):
          raise ValueError("x_values and y_values must have the same length")
      elif(len(set(x_values)) != len(y_values)):
        raise ValueError("x_Values must be unique")
      
      n = len(x_values)  # Number of points
      P_x = 0 

      for i in range(n):
          L_i = 1
          for j in range(n):
              if i != j:
                  L_i *= (x - x_values[j]) / (x_values[i] - x_values[j])

          P_x += y_values[i] * L_i

      return P_x

  # divided difference
  def divided_difference(self,x_values, y_values,x):
    
      # Check for edge cases:
      if len(x_values) != len(y_values):
          raise ValueError("x_values and y_values must have the same length.")
      
      if len(x_values) == 1:
          # With only one point, the polynomial is simply y = constant
          return [y_values[0]]

      n = len(x_values)
      divided_diff = [[0] * n for _ in range(n)]
      # column 0 will be marked with the f(x) values
      for i in range(n):
          divided_diff[i][0] = y_values[i]

      for j in range(1, n):
          for i in range(n - j):
              numerator = divided_diff[i + 1][j - 1] - divided_diff[i][j - 1]
              denominator = x_values[i + j] - x_values[i]
              if denominator == 0:
                  raise ZeroDivisionError("Duplicate x_values aren't allowed")
              divided_diff[i][j] = numerator / denominator

      # Extract the coefficients from the first row of the divided difference matrix(as only 1st row is reqd)
      coefficients = [divided_diff[0][j] for j in range(n)]
      result = coefficients[0]
      product_term = 1  #  (x - x0)(x - x1)...(x - xi)

      for i in range(1, n):
          product_term *= (x - x_values[i - 1])
          result += coefficients[i] * product_term
      return result
      
# Runge Kutta Family of methods
  def euler_method(self,x0, y0,x_to_Cal, n,func):
    
    # Solving the ODE y' = f(x, y) using Euler's method.

    f=eval(f"lambda x,y:{func}")
    solution = [(x0, y0)] #this list will contain solution of each step.
    x, y = x0, y0
    h=(x_to_Cal-x)/n
    
    for i in range(n):
        # Calculate the slope using f(x, y)
        y += h * f(x, y)   
        x += h             
        solution.append((x, y))
    
    return solution
  

  def heuns_method(self,x0, y0,x_to_Cal, n,func):
    
    # Solving the ODE y' = f(x, y) using heun's method.

    f=eval(f"lambda x,y:{func}")
    solution = [] #this list will contain solution of each step.
    x1, y1 = x0, y0
    h=(x_to_Cal-x1)/n
    
    for _ in range(n+1):
      solution.append((x1, y1))
      # Calculate the slope using f(x, y)
      s1=f(x1,y1)
      x2,y2=x1+h,y1+h*s1
      s2=f(x2,y2)
      y2=y1+h*(s1+s2)/2
      x1,y1=x2,y2
    return solution
  