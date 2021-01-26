%% ASEN 3111 Aerodynamics Computational Assignment 3 - NACA_Airfoils.m
% The purpose of this function is to generate arrays of x and y values of
% boundary points to be used in a vortex panel method. The function uses
% parameters from naca four digit airfoils to determine the shape and
% select boundary points.
%
%   Author: Andrew Thompson
%   Created: 10/9/2020  Edited: 10/26/2020
%   Note: Parameters m, p, t should be normalized by chord length
%
%   Parameters:     m <double> - Maximum camber
%                   p <double> - Location of maximum camber
%                   t <double> - Maximum thickness
%                   c <double> - Chord length
%                   N <double> - Number of boundary points
%
%   Outputs:        x [N x 1] <double> - The x locations of boundary points
%                   y [N x 1] <double> - The y locations of boundary points
%

function [x,y] = NACA_Airfoils(m,p,t,c,N)
    %% Anonymous Functions 
    % Thickness
    ytFunc = @(x) (t*c/0.2)*(0.2969*sqrt(x/c)-0.1260*(x/c)-0.3516*(x/c)^2+0.2843*(x/c)^3-0.1036*(x/c)^4);
    % Camber for x < max camber
    yc1Func = @(x) m*(x/p^2)*(2*p-(x/c));
    % Camber for x > max camber
    yc2Func = @(x) m*((c-x)/(1-p)^2)*(1+(x/c)-2*p);
    % Slope of airfoil
    dydxFunc = @(x1,yc1,x,yc) (yc1-yc)/(x1-x);
    % Angle of slope
    zetaFunc = @(dydx) atan(dydx);
    
    %% Initialize Variables & Constants
    % Initialize vectors for points 
    x = zeros(N, 1); y = zeros(N, 1);
    % Define step size 
    stepSize = c/N;
    % Initialize index 
    index = 1;
    
    %% Coordinate Computations
    % For all x values between origin and chord length
    for xStep = [linspace(c, 0, floor(N/2)) linspace(stepSize, c, ceil(N/2))]
        % If the airfoil is symmetric
        if m == 0 && p == 0
            % x value is just the current step
            x(index) = xStep;
            % If on the lower surface
            if index <= floor(N/2)
                % Use negative thickenss for y
                y(index) = -ytFunc(xStep);
            % If on the upper surface
            else
                % Use positive thickness for y
                y(index) = ytFunc(xStep);
            end
        % If the airfoil is non symmetric
        else
            % Get the thickness
            yt = ytFunc(xStep);
            % If current x less than max camber
            if xStep <= p*c
                % Calculate camber from function 1
                yc1 = yc1Func(xStep);
                yc = yc1Func(xStep+stepSize);
            % If current x greater than max camber
            else
                % Calculate camber from function 2
                yc1 = yc2Func(xStep);
                yc = yc2Func(xStep+stepSize);
            end
            % Calculate the slope of the camber
            dydx = dydxFunc(xStep+stepSize,yc1,xStep,yc);
            % Calculate the angle of slope 
            zeta = zetaFunc(dydx);
            if index <= floor(N/2)
                % Lower values
                x(index) = xStep + yt*sin(zeta);
                y(index) = yc1 - yt*cos(zeta);
            else
                % Upper values
                x(index) = xStep - yt*sin(zeta);
                y(index) = yc1 + yt*cos(zeta);
            end
        end
        % Increment Index
        index = index + 1;
    end
end


