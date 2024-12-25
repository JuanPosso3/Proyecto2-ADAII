include "data.dzn";

%Juan Miguel Posso -2259610
%Jhon Alejandro Martinez -2259565
% Modelo en MiniZinc para ubicar nuevos programas de ingeniería de sistemas

% Parámetros de entrada
int: num_existing_locations; % Número de localizaciones existentes
array[0..num_existing_locations-1, 0..1] of int: existing_locations; % Coordenadas de localizaciones existentes
int: matrix_size; % Tamaño de las matrices de segmento de población y entorno empresarial
array[0..matrix_size-1, 0..matrix_size-1] of int: population_matrix; % Matriz de segmento de población
array[0..matrix_size-1, 0..matrix_size-1] of int: business_matrix; % Matriz de entorno empresarial
int: num_new_programs; % Número de programas a ubicar

% Variables
array[0..num_new_programs-1, 0..1] of var 0..matrix_size-1: new_locations; % Coordenadas de los nuevos programas

% Calcular la ganancia inicial usando las ubicaciones existentes
int: initial_gain = sum([let {
    set of int: x_range = max(0, existing_locations[i, 1]-1)..min(matrix_size-1, existing_locations[i, 1]+1),
    set of int: y_range = max(0, existing_locations[i, 0]-1)..min(matrix_size-1, existing_locations[i, 0]+1)
} in
    sum([population_matrix[x, y] + business_matrix[x, y] | x in x_range, y in y_range])
| i in 0..num_existing_locations-1]);

% Calcular la ganancia total considerando las nuevas ubicaciones
var int: total_gain = sum([let {
    var set of int: x_range = max(0, new_locations[i, 1]-1)..min(matrix_size-1, new_locations[i, 1]+1),
    var set of int: y_range = max(0, new_locations[i, 0]-1)..min(matrix_size-1, new_locations[i, 0]+1)
} in
    sum([population_matrix[x, y] + business_matrix[x, y] | x in x_range, y in y_range])
| i in 0..num_new_programs-1]) + sum([let {
    set of int: x_range = max(0, existing_locations[i, 1]-1)..min(matrix_size-1, existing_locations[i, 1]+1),
    set of int: y_range = max(0, existing_locations[i, 0]-1)..min(matrix_size-1, existing_locations[i, 0]+1)
} in
    sum([population_matrix[x, y] + business_matrix[x, y] | x in x_range, y in y_range])
| i in 0..num_existing_locations-1]);

% Restricciones
constraint
    % 1. Los nuevos programas no pueden estar contiguos a las localizaciones existentes
    forall(new_loc in 0..num_new_programs-1, existing_loc in 0..num_existing_locations-1) (
        abs(new_locations[new_loc, 0] - existing_locations[existing_loc, 0]) > 1 \/
        abs(new_locations[new_loc, 1] - existing_locations[existing_loc, 1]) > 1
    );

constraint
    % 2. Segmento de población no menor que 25
    forall(new_loc in 0..num_new_programs-1) (
        let {
            var set of int: x_range = max(0, new_locations[new_loc, 1]-1)..min(matrix_size-1, new_locations[new_loc, 1]+1),
            var set of int: y_range = max(0, new_locations[new_loc, 0]-1)..min(matrix_size-1, new_locations[new_loc, 0]+1)
        } in
            sum([population_matrix[i, j] | i in x_range, j in y_range]) >= 25
    );

constraint
    % 3. Entorno empresarial no menor que 20
    forall(new_loc in 0..num_new_programs-1) (
        let {
            var set of int: x_range = max(0, new_locations[new_loc, 1]-1)..min(matrix_size-1, new_locations[new_loc, 1]+1),
            var set of int: y_range = max(0, new_locations[new_loc, 0]-1)..min(matrix_size-1, new_locations[new_loc, 0]+1)
        } in
            sum([business_matrix[i, j] | i in x_range, j in y_range]) >= 20
    );

constraint
    % 4. Los nuevos programas no pueden estar contiguos entre sí
    forall(i in 0..num_new_programs-1, j in 0..num_new_programs-1 where i != j) (
        abs(new_locations[i, 0] - new_locations[j, 0]) > 1 \/
        abs(new_locations[i, 1] - new_locations[j, 1]) > 1 \/
        (abs(new_locations[i, 0] - new_locations[j, 0]) + abs(new_locations[i, 1] - new_locations[j, 1]) > 1)
    );

constraint
    % 5. Los nuevos programas deben estar en ubicaciones distintas
    forall(i in 0..num_new_programs-1, j in 0..num_new_programs-1 where i != j) (
        new_locations[i, 0] != new_locations[j, 0] \/ new_locations[i, 1] != new_locations[j, 1]
    );

% Función objetivo: Maximizar la ganancia total
solve maximize total_gain;

% Salida
output [
    "Ganancia inicial: ", show(initial_gain),
    "\nUbicaciones nuevas:\n" ++ join("\n", [show(new_locations[i, 0]) ++ " " ++ show(new_locations[i, 1]) | i in 0..num_new_programs-1]),
    "\nGanancia total: ", show(total_gain)
];
