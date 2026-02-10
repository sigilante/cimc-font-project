% ==============================================================================
% U+10400 DESERET CAPITAL LETTER LONG I (𐐀)
% Perdita specimen extraction
% ==============================================================================

input perdita_base.mp;

beginfig(1024);  % 66560 modulo 65536
  
  % --- SCALE PARAMETERS ---
  x_scale = 36;
  y_scale = 72;
  
  % --- PATH CONTROL POINTS ---
  
  numeric start_x, start_y;
  numeric upper_x, upper_y;
  numeric right_x, right_y;
  numeric bottom_x, bottom_y;
  numeric left_x, left_y;
  
  numeric left_y_coeff;  % Coefficient for left_y position
  
  left_y_coeff := 0.5;  % Initial guess (to be optimized)
  
  start_x := -x_scale;
  start_y := y_scale;
  
  upper_x := 0;
  upper_y := y_scale;
  
  right_x := x_scale;
  right_y := 0;
  
  bottom_x := 0;
  bottom_y := -y_scale;
  
  left_x := -x_scale;
  left_y := -left_y_coeff * y_scale;  % Now optimizable
  
  % --- PEN SIZES ---
  
  numeric pen_start, pen_loop, pen_right, pen_bottom, pen_left;
  
  pen_start := 12;
  pen_loop := 10;
  pen_right := 14;
  pen_bottom := 14;
  pen_left := 14;
  
  % --- TENSION PARAMETERS ---
  
  t1 := 1.1;
  t2 := 1.2;
  t3 := 1.1;
  t4 := 1.0;
  t5 := 1.1;
  
  % --- CONSTRUCT CENTERLINE PATH ---
  
  path centerline;
  
  centerline := (start_x, start_y){down}
                -- (start_x, start_y - 0.25*y_scale)
                .. tension t1
                .. (upper_x, upper_y){right}
                .. tension t2
                .. (right_x, right_y){down}
                .. tension t3
                .. (bottom_x, bottom_y){left}
                .. tension t4
                .. (left_x, left_y){up}
                .. tension t5
                .. (right_x, right_y){right};
  
  % --- DRAW WITH VARIABLE PEN ---
  
  numeric n_segments, plen, i;
  numeric t_start, t_end, t_mid;
  numeric current_pen_size;
  
  n_segments := 30;
  plen := length(centerline);
  
  for i = 0 upto n_segments - 1:
    t_start := (i / n_segments) * plen;
    t_end := ((i + 1) / n_segments) * plen;
    t_mid := (t_start + t_end) / 2;
    
    if t_mid < 1:
      current_pen_size := pen_start;
    elseif t_mid < 2:
      current_pen_size := pen_loop + (pen_right - pen_loop) * (t_mid - 1);
    elseif t_mid < 3:
      current_pen_size := pen_right + (pen_bottom - pen_right) * (t_mid - 2);
    elseif t_mid < 4:
      current_pen_size := pen_bottom + (pen_left - pen_bottom) * (t_mid - 3);
    else:
      current_pen_size := pen_left + (pen_start - pen_left) * ((t_mid - 4) / (plen - 4));
    fi;
    
    if t_mid < 0.5:
      pickup pensquare scaled current_pen_size rotated 0;
    else:
      pickup pencircle scaled current_pen_size;
    fi;
    
    draw subpath (t_start, t_end) of centerline;
  endfor;
  
endfig;

end;