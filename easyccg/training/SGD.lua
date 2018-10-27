local SGD = torch.class('nn.SGD')

function SGD:__init(module, criterion, folder, numberOfLookupTables)
   self.learningRate = 0.01
   self.learningRateDecay = 0
   self.maxIteration = 25
   self.shuffleIndices = true
   self.module = module
   self.criterion = criterion
   self.folder = folder
   self.log=io.open(folder .. '/log',"w")
   self.log:setvbuf("no") 
   self.numberOfLookupTables = numberOfLookupTables
   self.window = window
end


function SGD:eval(validation)
       right = 0.0
       for t = 1,validation:size() do
         local input = validation[1][t]
         local target = validation[2][t]
         local newInput = self:processInput(input)
         output = self.module:forward(newInput)

         outputLabel = 1;
         outputValue = output[1];

         for k=2,output:storage():size() do
           if output[k] > outputValue then
	     outputLabel = k;
             outputValue = output[k];
           end
         end

         if(outputLabel == target) then
           right = right + 1;
         end
      end   
      accuracy = right / validation:size()
      return accuracy
end

function SGD:logLikelihood(validation)
       result = 0.0
       for t = 1,validation:size() do
         local example = validation[t]
         local input = example[1]
         local target = example[2]
         output = self.module:forward(input)
         if (target <= output:storage():size()) then
           result = result + math.log(output[target])
         end

      end   
      return result
end

function SGD:processInput(input)
  -- Input is a big one-dimensional tensor.
  -- The first window*numberOfLookupTables inputs are indices into torch lookup-tables, with trainable parameters.
  -- The remaining input is used directly by the classification layer.
  -- We have to do it in this painful way because Lua can't cope with lots of table objects.
  local lookupTableInput = input:narrow(1,1,self.numberOfLookupTables * window)
  local newInput = nn.SplitTable(1):forward(nn.Reshape(self.numberOfLookupTables,window):forward(lookupTableInput))

  local lengthOfIndexInput = input:size(1) - (self.numberOfLookupTables * window)
  if lengthOfIndexInput > 0 then
    -- Twiddle around with the shape of the rest of the input, to make it look like Torch expects.
    newInput[4] = nn.Reshape(window, lengthOfIndexInput / window):forward(input:narrow(1,self.numberOfLookupTables * window + 1, lengthOfIndexInput))
  end

  return newInput
end

function SGD:train(dataset, validation)
   self.log:write("# SGD: training" .. '\n')   
   local iteration = 1
   local currentLearningRate = self.learningRate
   local module = self.module
   local criterion = self.criterion

   local shuffledIndices = torch.randperm(dataset:size(), 'torch.LongTensor')
   if not self.shuffleIndices then
      for t = 1,dataset:size() do
         shuffledIndices[t] = t
      end
   end

   bestScore = -1;
   it = 0;
   local itsSinceImprovement = 0;
   while true do
      it = it + 1
      self.log:write("Iteration " .. it .. " ")

      
      local currentError = 0
      for t = 1,dataset:size() do

         local input = dataset[1][shuffledIndices[t]]
         local target = dataset[2][shuffledIndices[t]]

         local newInput = self:processInput(input)

         currentError = currentError + criterion:forward(module:forward(newInput), target)

         module:updateGradInput(newInput, criterion:updateGradInput(module.output, target))
         module:accUpdateGradParameters(newInput, criterion.gradInput, currentLearningRate)

         if self.hookExample then
            self.hookExample(self, example)
         end
      end

      if self.hookIteration then
         self.hookIteration(self, iteration)
      end

      currentError = currentError / dataset:size()
      self.log:write("# current error = " .. currentError .. '\n')

      acc=self:eval(validation)

      self.log:write("Development Set Accuracy: " .. acc .. '\n')


      if acc > bestScore then
        torch.save(folder .. '/bestModel', self.module) 
        bestScore=acc
        itsSinceImprovement = 0
      else 
        itsSinceImprovement = itsSinceImprovement + 1
      end

      iteration = iteration + 1
      currentLearningRate = self.learningRate/(1+iteration*self.learningRateDecay)
      if self.maxIteration > 0 and iteration > self.maxIteration then
         self.log:write("# SGD: you have reached the maximum number of iterations" .. '\n')
         break
      end

     if itsSinceImprovement == 1 then
         self.log:write("# SGD: no improvement for 1 iteration. Stopping training." .. '\n')
         break
     end
   end
end

