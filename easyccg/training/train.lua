require 'torch'
require 'nn'
require 'features'
require 'SGD'


local Train = torch.class('nn.Train')
-- read input files
function Train:loadDataset(path, features, windowBackward, windowForward, includeRareCategories) 
  file = io.open(path)
  local lineNum = 1;
  local size = 0;
   for line in file:lines() do 
    if lineNum > 3 or (line ~= '' and string.sub(line, 1, 1) ~= '#') then
     for instance in string.gmatch(line, "[^ ]+") do
       size = size + 1
     end
    end
    lineNum = lineNum + 1
   end

  
  -- Get length of input

  file = io.open(path)
  local index = 0
  local window = windowBackward + windowForward + 1

  local inputData = torch.Tensor(size, window * (3 + features:getNumberOfSparseFeatures()))
  local targetData = torch.IntStorage(size)

  local lineNum = 1;
   for line in file:lines() do 
    if lineNum > 3 or (line ~= '' and string.sub(line, 1, 1) ~= '#') then

     local numWords = 0
     local words = {}
     local cats = {}
     local posTags = {}
     for instance in string.gmatch(line, "[^ ]+") do 
       numWords = numWords + 1

       local delim1 = string.find(instance, '|', 1, true)
       
       if (delim1) then
         local delim2 = string.find(instance, '|', delim1 + 1, true)

         words[numWords] = string.sub(instance, 1, delim1 - 1)

         if (delim2) then
           posTags[numWords] = string.sub(instance, delim1 + 1, delim2 - 1)
           cats[numWords] = string.sub(instance, delim2 + 1, string.len(instance))
         else
           posTags[numWords] = string.sub(instance, delim1 + 1, string.len(instance))
         end
       else
         -- No training example provided
         cats[numWords] = "*NO_CATEGORY*"
         words[numWords] = instance
       end
     end

     
     for i = 1,numWords do
        
        local input = features:getFeatures(words, posTags, i, windowBackward, windowForward);
        local label = features:getCategoryIndex(cats[i])

        if label > 0 or (includeRareCategories) then
          --Label 0 is rare categories. These are used for evaluation, but not for training.
          index = index + 1

          for j=1,input:size()[1] do 
            value = input[j]
            inputData[index][j] = value
          end

          targetData[index] = label
        end      
     end
else

    end
    lineNum = lineNum + 1
   end
  local dataset = {inputData, targetData};
  function dataset:size() return (index) end

  return dataset
end


function Train:loadEmbeddings(path)
  local file = io.open(path)
  local firstLine = file:read("*line");
  local embeddingsSize = 0

  for instance in firstLine.gmatch(firstLine, "[^ ]+") do
    embeddingsSize = embeddingsSize + 1
  end


  embeddingsFile = torch.DiskFile(path);
  wordTable = nn.LookupTable(features.numWords, embeddingsSize)
  embedding = torch.DoubleStorage(embeddingsSize)
  print("Loading embeddings")

  for i=1,features.numWords-1-features.extraWords do

     embeddingsFile:readDouble(embedding);
     local emb = torch.Tensor(embeddingsSize)
     for j=1,embeddingsSize do 
        emb[j] = embedding[j]
     end
     --First two entries are padding
     if i==1 then
       for j=1,features.extraWords do
         wordTable.weight[j] = emb:clone();
       end
     end
    wordTable.weight[i + features.extraWords] = emb;
  end
  print("Loaded embeddings")
  return wordTable, embeddingsSize
end



function Train:trainModel(trainFile, validationAutoFile, validationGoldFile, embeddingsFolder, features, windowBackward, windowForward, hiddenSize, name)

  wordTable, embeddingsSize = self:loadEmbeddings(embeddingsFolder .. '/embeddings.vectors')
  k = 5
  window = windowBackward +  windowForward + 1
  tableSize = (embeddingsSize + k + k + features:getNumberOfSparseFeatures()) * window
  print ("Window Size  = " .. window)
  print ("Embeddings Size  = " .. embeddingsSize)
  print ("Lookup Table Size  = " .. tableSize)
  print ("Categories Size  = " .. features.numCats)
  print ("Suffixes Size  = " .. features.numSuffixes)
  print ("Vocabulary Size  = " .. features.numWords)
  print ("Sparse Features Size  = " .. features:getNumberOfSparseFeatures())

  capsTable = nn.LookupTable(window, k)
  capsTable:reset(0.1)
  suffixTable = nn.LookupTable(features.numSuffixes, k)
  suffixTable:reset(0.1)
  pt = nn.ParallelTable()
  pt:add(wordTable)
  pt:add(suffixTable)
  pt:add(capsTable)

  -- Assume we always have 3 lookup-table features (word embeddings, suffixes and capitalization), 
  -- but allow additional features (such as word, POS and Brown clusters) as one-hot vectors.
  if features:getNumberOfSparseFeatures() > 0 then
    pt:add(nn.Identity())
  end

  jt = nn.JoinTable(2)
  rs2 = nn.Reshape(tableSize)
  mlp = nn.Sequential()
  mlp:add(pt)
  mlp:add(jt)
  mlp:add(rs2)

  if hiddenSize > 0 then
    ll1 = nn.Linear(tableSize, hiddenSize)
    hth = nn.HardTanh()
    ll2 = nn.Linear(hiddenSize, features.numCats)
    lsm = nn.LogSoftMax()

    mlp:add(ll1)
    mlp:add(hth)
    mlp:add(ll2)
    mlp:add(lsm)

  else 
    hth = nn.HardTanh()
    ll1 = nn.Linear(tableSize, features.numCats)
    lsm = nn.LogSoftMax()
    mlp:add(ll1)
    mlp:add(lsm)
  end  

  folder = embeddingsFolder .. '/train.' .. name --.. hiddenSize .. '.' .. windowBackward .. '.' .. windowForward
  os.execute("mkdir " .. folder)

  print ("Loading dev set")
  -- Hacky way of merging automatic POS tags with Gold supertags
  local validationAuto = self:loadDataset(validationAutoFile, features, windowBackward, windowForward, true)
  local validationGold = self:loadDataset(validationGoldFile, features, windowBackward, windowForward, true)
  local validation = {validationAuto[1], validationGold[2]}
  function validation:size() return (validationAuto:size()) end
  print ("Dev examples: " .. validation:size())

  print ("Loading train set")
  dataset = self:loadDataset(trainFile, features, windowBackward, windowForward, false)
  print ("Done")


  criterion = nn.ClassNLLCriterion()
  trainer = nn.SGD(mlp, criterion, folder, 3, window)
  trainer.learningRate = 0.01
  trainer.maxIteration = 25
  trainer:train(dataset, validation)
  return mlp

end

