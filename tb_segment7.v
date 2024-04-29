`timescale 1ns / 1ps

module tb_segment7;

    reg [3:0] bcd;
    wire [6:0] seg;
    integer file_bcd, file_seg, scan_file;

    bcd_to_7seg uut (
        .bcd(bcd), 
        .seg(seg)
    );

    initial begin
        file_bcd = $fopen("bcd_value.dat", "r");
        file_seg = $fopen("seg_output.dat", "w");
        if (file_bcd == 0 || file_seg == 0) begin
            $display("Error: Can't open file.");
            $finish;
        end
        while (!$feof(file_bcd)) begin
            scan_file = $fscanf(file_bcd, "%b\n", bcd);
            #10; // Simulate some time passing
            $fwrite(file_seg, "%b\n", seg);
            $display("BCD: %b, Segments: %b", bcd, seg); // Debugging line
        end
        $fclose(file_bcd);
        $fclose(file_seg);
        $finish;
    end

endmodule
