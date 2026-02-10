% U+0028 LEFT PARENTHESIS (()
beginfig(40) ;
  pickup thin_pen;
  path lparen;
  lparen := ((1/3)*x_radius, y_radius){left}
            .. tension 0.9
            .. (-(1/3)*x_radius, Oy){down}
            .. tension 0.9
            .. ((1/3)*x_radius, -y_radius){right};
  draw lparen;
endfig;
