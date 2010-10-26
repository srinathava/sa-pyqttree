function dumpPerf(fname)
    d = load(fname);
    [p, fnameWoext] = fileparts(fname);
    fp = fopen(fullfile(p, [fnameWoext '.raw']), 'w');
    
    vec = d.PerformanceTracingRawDataVector;
    
    initTime = vec{1}{10};
    for i=1:length(vec)
        stage = vec{i}{2};
        mainMachine = vec{i}{4};
        target = vec{i}{5};
        machine = vec{i}{6};
        chart = vec{i}{7};
        wallClockTime = vec{i}{10};
        isBegin = vec{i}{9};
        
        fprintf(fp, '%s:', target, mainMachine, machine, chart, stage);
        if isBegin
            fprintf(fp, 'begin');
        else
            fprintf(fp, 'end');
        end
        fprintf(fp, '\t%f\n', wallClockTime - initTime);
    end
end