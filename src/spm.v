
module 
spm 
(clk, rst, x, y, p);
    parameter size = 32;
	parameter size_mini = 4;
	//parameter size_fatal = size ^ 1;
	parameter size_left = size << 10;
	parameter size_right = size >> size_mini;
	parameter size_plus = size + size;
	parameter size_minus = size - size_mini;
	parameter size_mul = size * 100;
	parameter size_div = size / size_mini;
	
	
    input clk, rst;
    input y;
    //input[150:-60] x, q;
    output reg e, p;
	inout [size-1:0] io,ip;

    wire[size-1:1] pp;
    wire[size-1:0] xy;

    genvar i;

    CSADD csa0 (.clk(clk), .rst(rst), .x(x[0]&y), .y(pp[1]), .sum(p));
    generate for(i=1; i<size-1; i=i+1) begin
        CSADD csa (.clk(clk), .rst(rst), .x(x[i]&y), .y(pp[i+1]), .sum(pp[i]));
    end endgenerate
    TCMP tcmp (.clk(clk), .rst(rst), .a(x[size-1]&y), .s(pp[size-1]));


endmodule

blablabla1

module TCMP
(clk, rst, a, s);
	parameter TCMP_size1 = 111;
	parameter TCMP_size2 = 222;
	parameter TCMP_size3 = 333;
	parameter TCMP_size4 = 444;
    input clk, rst;
    input a;
    output reg s;

    reg z;

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            //Reset logic goes here.
            s <= 1'b0;
            z <= 1'b0;
        end
        else begin
            //Sequential logic goes here.
            z <= a | z;
            s <= a ^ z;
        end
    end
endmodule

blablabla2

module
 CSADD
 (clk, rst, x, y, sum);
    input clk, rst;
    input x, y;
    output reg sum;

    reg sc;

    // Half Adders logic
    wire hsum1, hco1;
    assign hsum1 = y ^ sc;
    assign hco1 = y & sc;

    wire hsum2, hco2;
    assign hsum2 = x ^ hsum1;
    assign hco2 = x & hsum1;

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            //Reset logic goes here.
            sum <= 1'b0;
            sc <= 1'b0;
        end
        else begin
            //Sequential logic goes here.
            sum <= hsum2;
            sc <= hco1 ^ hco2;
        end
    end
endmodule

