  % Values arbitrarily chosen. It's a useful exercise to vary these and look at the results
  T_final = 300;
  N_t = 2000;
  X_final = 1;
  N_x = 100;
  
  % Calculate time and x steps based on sampling size and # of samples
  T = linspace(0, T_final, N_t+1);
  X = linspace(0, X_final, N_x+1);
  dt = T(2) - T(1);  % Calculate delta t
  dx = X(2) - X(1);  % Calculate delta x

  alpha = 9.7e-5; % Thermal diffusivity of Aluminium in m^2/s
  Fo = (alpha*dt)/(dx^2); % Fouriers number = diffusive transport rate/storage rate
 
  % Define your initial condition here. This could be some function IC(x),
  %  however for simplicity's sake we take a rod with a uniform temperature
  %  and in contact with a hot plate at one end
  wall_temp = 200;
  init_temp = 25;
  
  % Initialize the N state and the N-1 state
  u_old = zeros(1, N_x+1); 
  u_old(:) = init_temp;
  u_old(1) = wall_temp;
  u_cur = u_old;
  u_plot = u_old;

  for t = 1:N_t
     for i = 2:N_x
     	 % Forward Euler solution to heat equation
         u_cur(i) = Fo*(u_old(i+1) - 2*u_old(i) + u_old(i-1)) + u_old(i);
     end
     u_cur(1) = wall_temp; % Set the left boundary to be our high of 200 
     u_old(:) = u_cur; % We move to the next time step, reset N-1 state
     u_plot = [u_plot; u_cur];
  end

  [X_plot,T_plot] = meshgrid(X,T); % Create 2D meshgrid to create surface plot

  surf(X_plot,T_plot,u_plot,'EdgeColor','none') % Create surface plot
  c = colorbar; % Attach colour bar and create scale
  c.Label.String = 'Temperature [C]';

  xlim([0 1]) % Add axis limits
  xlabel('Distance along rod [m]'); % Add descriptive axis labels
  ylabel('Time [s]');
  zlabel('Temperature [C]')
