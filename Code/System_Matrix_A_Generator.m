%j = 3;
%n = 2^(2*j);
j = 9;
n = 81;

%Nang = 33;
Nang = 36;
angles = [0:(Nang-1)]*360/Nang;

%tmp = radon(zeros(2^j, 2^j), angles);
tmp = radon(zeros(j, j), angles);
k = length(tmp(:));
%disp(length(angles(:)));

A = sparse(k, n);
k
n
%disp(length(A))

for iii = 1:n
   %unitvec = zeros(2^j, 2^j);
   unitvec = zeros(j, j);
   unitvec(iii) = 1;
   
   tmp = radon(unitvec, angles);
   %length(tmp(:))
   A(:, iii) = sparse(tmp(:));
end

figure(1)
clf
spy(A)